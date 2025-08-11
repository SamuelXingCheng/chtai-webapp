# backend/app/services/lifestudy_parser.py
import re
import sys
import unicodedata
from typing import Tuple, List, Dict, Any

# ===== 你可以調整的輸出樣式 =====
FORMAT_LEVEL1 = "{marker}、{text}"        # 大點：壹、...
FORMAT_LEVEL2 = "  • {marker}、{text}"    # 中點：  • 一、...
FORMAT_LEVEL3 = "    - {marker}. {text}"  # 小點：    - 1. ...
# =================================

# 支援的綱目樣式（含常見括號、標點變體）
# 大點：壹貳參(参)肆伍陸柒捌玖拾
RE_L1 = re.compile(
    r"""^\s*
        [\(\（\[\{]?
        (?P<mk>壹|貳|參|参|肆|伍|陸|柒|捌|玖|拾)
        (?:[、．\.\:：\)）]|[\s\u3000\u00A0]+)     # ← 必須有分隔符或至少一空白
        (?P<txt>.+?)
        \s*$
    """, re.X
)

# 中點：一二三四五六七八九十
RE_L2 = re.compile(
    r"""^\s*
        [\(\（\[\{]?
        (?P<mk>一|二|三|四|五|六|七|八|九|十)
        (?:[、．\.\:：\)）]|[\s\u3000\u00A0]+)     # ← 必須有分隔符或至少一空白
        (?P<txt>.+?)
        \s*$
    """, re.X
)

# 小點：阿拉伯數字 1~99
RE_L3 = re.compile(
    r"""^\s*
        [\(\（\[\{]?
        (?P<mk>\d{1,2})
        (?:[、．\.\:：\)）]|[\s\u3000\u00A0]+)     # ← 必須有分隔符或至少一空白
        (?P<txt>.+?)
        \s*$
    """, re.X
)

def _normalize_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00A0", " ")  # NBSP → space
    s = s.replace("\u3000", " ")  # 全形空白 → space
    s = s.replace(",", "，").replace(":", "：").replace("?", "？").replace("!", "！").replace(";", "；")
    return s

def _prebreak_outline_markers(s: str) -> str:
    # 你原本的三段預切邏輯...
    s = re.sub(
        r'(?<!^)(?<!\n)\s*(?=(壹|貳|參|参|肆|伍|陸|柒|捌|玖|拾)(?=[ 　、．\.\:：\)\）\-–—]))',
        '\n\n', s
    )
    s = re.sub(
        r'(?<!^)(?<!\n)\s*(?=(一|二|三|四|五|六|七|八|九|十)(?=[ 　、．\.\:：\)\）\-–—]))',
        '\n\n', s
    )
    s = re.sub(
        r'(?<!^)(?<!\n)\s*(?=(\d{1,2})(?=[ 　、．\.\:：\)\）\-–—]))',
        '\n\n', s
    )

    # 👉 新增：把「雙半形空白以上」視為段落分隔（轉成空白行）
    # 只在「左右都是非空白字元」時才生效，避免行首/行尾的多空白誤判。
    s = re.sub(r'(?<=\S) {2,}(?=\S)', '\n\n', s)

    return s

def _split_blocks(s: str) -> List[str]:
    """
    以「空白行」為段落切割；同段內行與行之間以空白合併。
    僅含空白的段落會被丟棄。
    """
    raw_blocks = re.split(r"\n\s*\n", s.strip(), flags=re.M)
    blocks: List[str] = []
    for b in raw_blocks:
        # 去除每行多餘空白，並把同段多行合併為一句（保留單一空格）
        lines = [ln.strip() for ln in b.split("\n")]
        lines = [ln for ln in lines if ln]  # 移除空行
        if not lines:
            continue
        merged = re.sub(r"\s+", " ", " ".join(lines)).strip()
        if merged:
            blocks.append(merged)
    return blocks

def _detect_level(block: str) -> Tuple[int, str, str]:
    """
    回傳：(level, marker, text)
    level: 1/2/3 或 0（一般段落）
    marker: 偵測到的綱目標記（如「壹」「一」「1」），一般段落則為空字串
    text: 去掉標記後的主體文字（一般段落則為原文）
    """
    m = RE_L1.match(block)
    if m:
        return 1, m.group("mk"), m.group("txt")

    m = RE_L2.match(block)
    if m:
        return 2, m.group("mk"), m.group("txt")

    m = RE_L3.match(block)
    if m:
        return 3, m.group("mk"), m.group("txt")

    return 0, "", block
def _split_heading_body(level: int, txt: str):
    """
    把像「身體  以弗所書的主題是召會。」拆成 title/body。
    但若是「主題─召會」這種「破折號 + 短詞」的情況，視為整個都是標題。
    """
    if level not in (1, 2, 3):
        return txt.strip(), ""

    s = txt.strip()

    def looks_like_short_title(word: str) -> bool:
        # 右側若很短、且不像句子（無終止標點、無明顯空白/多詞），就當作標題片語
        w = word.strip()
        if len(w) == 0:
            return False
        if len(w) <= 12 and not re.search(r"[。？！；;]", w) and not re.search(r"\s", w):
            return True
        return False

    # 1) 破折號（─ — -）預拆
    m = re.match(r'^(?P<title>[^，。；：:、\s]{1,30})\s*[─—-]\s*(?P<body>.+)$', s)
    if m:
        title, body = m.group('title').strip(), m.group('body').strip()
        # 回退：若右側像「召會」「引言」這類短詞，保留整段為標題
        if looks_like_short_title(body):
            return s, ""
        return title, body

    # 2) 冒號（： :）預拆
    m = re.match(r'^(?P<title>[^，。；：:、\s]{1,30})\s*[：:]\s*(?P<body>.+)$', s)
    if m:
        title, body = m.group('title').strip(), m.group('body').strip()
        # 冒號也做同樣回退，避免「篇題：召會」被錯拆
        if looks_like_short_title(body):
            return s, ""
        return title, body

    # 3) 單一空白分隔（全/半形），保留原規則
    m = re.match(r'^(?P<title>[^\s\u3000\u00A0]{1,30})[\s\u3000\u00A0]+(?P<body>.+)$', s)
    if m:
        title, body = m.group('title').strip(), m.group('body').strip()
        # 若右側是短詞，也回退為整段標題
        if looks_like_short_title(body):
            return s, ""
        return title, body

    # 拆不到就整段視為標題
    return s, ""


def parse_lifestudy_to_paragraphs(text: str) -> List[Dict[str, Any]]:
    """
    將原文解析為段落物件陣列：
      { level: 0|1|2|3, marker: str, text: str }
    規則補強：
    - 綱目標記後「正好一個空白」 ⇒ 視為標題分隔
    - 綱目標記後「兩個以上空白」 ⇒ 視為換段（標題留空，後面成為下一段，並插入換行）
    """
    text = _normalize_text(text)
    text = _prebreak_outline_markers(text)

    # 自行分段：保留每行內的連續空白，不做 \s+ 壓縮
    raw_blocks = re.split(r"\n\s*\n", text.strip(), flags=re.M)
    blocks: List[str] = []
    for b in raw_blocks:
        lines = [ln.strip() for ln in b.split("\n") if ln.strip()]
        if not lines:
            continue
        merged = " ".join(lines)
        if merged:
            blocks.append(merged)

    out: List[Dict[str, Any]] = []

    for b in blocks:
        level, mk, body = _detect_level(b)

        if level in (1, 2, 3):
            m_space = re.match(
                rf'^\s*[\(\（\[\{{]?{re.escape(mk)}[、．\.\:：\)\）]?\s*(?P<sep>[ \t]+)(?P<txt>.+?)\s*$',
                b
            )

            if m_space:
                sep = m_space.group("sep")
                txt_after = m_space.group("txt").strip()

                if len(sep) == 1:
                    # 單一空白 ⇒ 標題 + 內文
                    title, tail = _split_heading_body(level, txt_after)
                    out.append({"level": level, "marker": mk, "text": title})
                    if tail:
                        out.append({"level": 0, "marker": "", "text": tail})
                    continue

                elif len(sep) >= 2:
                    # 多於一個空白 ⇒ 換段
                    out.append({"level": level, "marker": mk, "text": ""})
                    if txt_after:
                        out.append({"level": 0, "marker": "", "text": txt_after})
                    # 插入一個空段落（代表換行）
                    out.append({"level": 0, "marker": "", "text": "\n"})
                    continue

            # 預設走原本拆法
            title, tail = _split_heading_body(level, body)
            out.append({"level": level, "marker": mk, "text": title})
            if tail:
                out.append({"level": 0, "marker": "", "text": tail})

        else:
            out.append({"level": 0, "marker": "", "text": body})

    return out

def parse_lifestudy(text: str) -> str:
    """
    回傳格式化後的單一字串（以 '\n' 分段）。
    """
    paragraphs = parse_lifestudy_to_paragraphs(text)

    out_lines: List[str] = []
    for p in paragraphs:
        lv, mk, body = p["level"], p["marker"], p["text"]
        if lv == 1:
            out_lines.append(FORMAT_LEVEL1.format(marker=mk, text=body))
        elif lv == 2:
            out_lines.append(FORMAT_LEVEL2.format(marker=mk, text=body))
        elif lv == 3:
            out_lines.append(FORMAT_LEVEL3.format(marker=mk, text=body))
        else:
            out_lines.append(body)
    return "\n".join(out_lines)


# --- 可直接當腳本使用 ---
if __name__ == "__main__":
    # 用法：
    # 1) 從檔案讀入： python lifestudy_parser.py < input.txt
    # 2) 直接貼上到 stdin
    src = sys.stdin.read()
    result = parse_lifestudy(src)
    print(result)