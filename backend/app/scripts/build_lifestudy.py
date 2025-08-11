# backend/app/scripts/build_lifestudy.py
# -*- coding: utf-8 -*-
"""
批次把 backend/app/data/lifestudy/raw/*.txt 或 *.json 解析成標準 JSON
- .txt：整篇文字 → paragraphs/text/html
- .json（{id,title,days:[{day,verse,content}] }）：逐天解析 content → paragraphs/text/html

預設輸出到 backend/app/data/lifestudy/processed/
用法：
  python backend/app/scripts/build_lifestudy.py
或指定輸入/輸出資料夾：
  python backend/app/scripts/build_lifestudy.py --in backend/app/data/lifestudy/raw --out backend/app/data/lifestudy/processed
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

# 從 services 匯入解析工具
from app.services.lifestudy_parser import (
    _normalize_text,
    _split_blocks,
    _detect_level,
    _prebreak_outline_markers,   # 先把非行首綱目前置換行
    parse_lifestudy_to_paragraphs
)

# ---- 共用轉換 ----
def parse_to_paragraphs(text: str):
    return parse_lifestudy_to_paragraphs(text)

def paragraphs_to_text(ps):
    from app.services.lifestudy_parser import FORMAT_LEVEL1, FORMAT_LEVEL2, FORMAT_LEVEL3
    lines = []
    for p in ps:
        lv, mk, body = p["level"], p["marker"], p["text"]
        if lv == 1: lines.append(FORMAT_LEVEL1.format(marker=mk, text=body))  # body = 標題
        elif lv == 2: lines.append(FORMAT_LEVEL2.format(marker=mk, text=body))
        elif lv == 3: lines.append(FORMAT_LEVEL3.format(marker=mk, text=body))
        else: lines.append(body)  # 一般正文
    return "\n".join(lines)


# ---- .json（raw） → processed 格式 ----
def process_raw_json(raw_path: Path, include_html: bool = True) -> dict:
    tz = timezone(timedelta(hours=8))
    raw = json.loads(raw_path.read_text(encoding="utf-8"))

    out = {
        "id": raw["id"],
        "title": raw["title"],
        "source": raw_path.name,
        "generatedAt": datetime.now(tz).isoformat(timespec="seconds"),
        "days": []
    }

    for d in raw.get("days", []):
        content_raw = d.get("content", "")
        ps = parse_to_paragraphs(content_raw)
        day_obj = {
            "day": d.get("day"),
            "verse": d.get("verse", ""),
            "contentRaw": content_raw,
            "paragraphs": ps,
            "text": paragraphs_to_text(ps),
        }
        out["days"].append(day_obj)

    return out

# ---- .txt → processed（舊流程保留） ----
def build_payload_from_txt(doc_id: str, title: str, source_name: str, paragraphs, include_html=True):
    tz = timezone(timedelta(hours=8))
    payload = {
        "id": doc_id,
        "title": title,
        "source": source_name,
        "generatedAt": datetime.now(tz).isoformat(timespec="seconds"),
        "paragraphs": paragraphs,
        "text": paragraphs_to_text(paragraphs),
    }

    return payload

# ---- CLI ----
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_dir", default="backend/app/data/lifestudy/raw", help="輸入資料夾（.txt 或 .json）")
    parser.add_argument("--out", dest="out_dir", default="backend/app/data/lifestudy/processed", help="輸出 JSON 資料夾")
    parser.add_argument("--title-prefix", default="生命讀經：", help="（僅 .txt 用）自動標題前綴，後面接檔名")
    parser.add_argument("--no-html", action="store_true", help="JSON 中不要 html 欄位")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 同時抓 txt + json
    files = sorted(list(in_dir.glob("*.txt")) + list(in_dir.glob("*.json")))
    if not files:
        print(f"⚠️ 找不到 .txt/.json 檔：{in_dir}")
        return

    count = 0
    for f in files:
        if f.suffix.lower() == ".json":
            # raw JSON → processed（含 days[]）
            payload = process_raw_json(f, include_html=not args.no_html)
            out_path = out_dir / f.name  # 直接沿用檔名
        else:
            # raw TXT → processed（整篇）
            raw_txt = f.read_text(encoding="utf-8")
            paragraphs = parse_to_paragraphs(raw_txt)
            doc_id = f.stem
            title = f"{args.title_prefix}{f.stem}"
            payload = build_payload_from_txt(doc_id, title, f.name, paragraphs, include_html=not args.no_html)
            out_path = out_dir / f"{doc_id}.json"

        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        count += 1
        print(f"✅ 產生：{out_path}")

    print(f"🎉 完成，共輸出 {count} 筆 JSON 到 {out_dir}")

if __name__ == "__main__":
    main()
