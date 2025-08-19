# weekly_parser.py
import json
import os
from docx import Document

from lxml import etree

class WeeklyParser:
    def __init__(self, file_path: str):
        self.doc = Document(file_path)
        self.sections = []
        self.current_section = None

    # ---------- 工具方法 ----------
    def _commit_section(self):
        """結束目前的 section 並存入 sections"""
        if self.current_section:
            self.sections.append(self.current_section)
            self.current_section = None

    def _new_section(self, title: str):
        """建立新的 section"""
        self._commit_section()
        self.current_section = {
            "type": "text",
            "title": title,
            "subtitle": "",
            "category": "truth",
            "content": ""
        }

    def _add_subtitle(self, subtitle: str):
        """設定副標題"""
        if self.current_section:
            self.current_section["subtitle"] = subtitle

    def _add_content(self, text: str):
        """加入內文"""
        if self.current_section:
            if self.current_section["content"]:
                self.current_section["content"] += "\n" + text
            else:
                self.current_section["content"] = text

    def _parse_intro(self, paragraphs):
        """解析開頭的話"""
        section = {
            "type": "text",
            "title": "開頭的話",
            "subtitle": "",
            "category": "truth",
            "content": ""
        }

        subtitles = []
        content_lines = []

        for i, para in enumerate(paragraphs):
            text = para.text.strip()
            if not text:
                continue
            style = para.style.name

            if style == "Normal":
                if len(subtitles) < 2:   # 前兩個 Normal 當 subtitle
                    subtitles.append(text)
                else:                    # 其餘 Normal 當 content
                    content_lines.append(text)

        # 👉 subtitle 用換行分隔
        section["subtitle"] = " ".join(subtitles)

        # 👉 content 用 \n 分隔每段
        section["content"] = "\n".join(content_lines)

        return section
    
    def _parse_progress_section(self, title, paragraphs, tables):
        section = {
            "type": "text",
            "title": title,
            "subtitle": "",
            "category": "truth",
            "content": ""
        }

        content_lines = []

        def extract_from_table(table, is_root=False):
            """遞迴解析表格"""
            lines = []
            for row in table.rows:
                # 🚩 收集這一列所有 cell 的文字
                row_texts = [p.text.strip() for cell in row.cells for p in cell.paragraphs if p.text.strip()]

                if is_root and row is table.rows[0] and row_texts and not section["subtitle"]:
                    # 第一列可能是 subtitle
                    section["subtitle"] = " ".join(row_texts)
                else:
                    if row_texts:
                        # 🚩 把這一列的所有 cell 用空格組合成一行
                        lines.append("".join(row_texts))

                # 🚩 檢查 cell 裡的子表格
                for cell in row.cells:
                    for subtable in cell.tables:
                        lines.extend(extract_from_table(subtable))
            return lines

        # 解析傳入的所有表格
        for table in tables:
            lines = extract_from_table(table, is_root=True)
            content_lines.extend(lines)

        section["content"] = "\n".join(content_lines)
        return section



        # ---------- 主流程 ----------
    def parse(self):
        # 收集 intro 段落直到第一個 Heading 2
        intro_paragraphs = []
        start_index = 0
        for i, para in enumerate(self.doc.paragraphs):
            if para.style.name == "Heading 2":
                start_index = i
                break
            intro_paragraphs.append(para)

        # 👉 先處理開頭的話
        intro_section = self._parse_intro(intro_paragraphs)
        self.sections.append(intro_section)

        # 👉 從第一個 Heading 2 開始解析剩下的內容
        i = start_index
        table_index = 0  # 追蹤表格
        while i < len(self.doc.paragraphs):
            para = self.doc.paragraphs[i]
            text = para.text.strip()
            style = para.style.name

            if not text:
                i += 1
                continue

            print(f"[{style}] {text[:50]}...")  # Debug

            if style == "Heading 2":
                if "本週晨興進度申言主題" in text:
                    # 收集段落直到「第二頁」或下一個 H2
                    block = []
                    i += 1
                    while i < len(self.doc.paragraphs):
                        p = self.doc.paragraphs[i]
                        if p.style.name == "Heading 2":  # 下一個大區塊
                            i -= 1
                            break
                        if "第二頁" in p.text:
                            break
                        block.append(p)
                        i += 1

                    # 🚩 找最近的一張表格（出現在這個 H2 之後）
                    tables = []
                    for t in self.doc.tables[table_index:]:
                        first_cell_text = t.cell(0, 0).text.strip()
                        print(f"DEBUG 表格第一格: {first_cell_text}")  # 可先印出檢查
                        if "週週福音" in first_cell_text or "台中市召會週訊" in first_cell_text:
                            table_index += 1
                            continue
                        # ✅ 確認到「第二十八週 神的奧祕－基督」的表格
                        tables = [t]
                        table_index += 1
                        break

                    progress_section = self._parse_progress_section(text, block, tables)
                    self.sections.append(progress_section)

                else:
                    # 一般 section
                    self._new_section(text)

            elif style == "Heading 3":
                self._add_subtitle(text)
            elif style == "Normal":
                self._add_content(text)

            i += 1

        self._commit_section()
        return self._build_result()





    def _build_result(self):
        return {
            "id": "2025-08-17",
            "title": "主後二〇二五年 八月十七日 台中市召會週訊 第2171期",
            "sections": self.sections
        }


if __name__ == "__main__":
    raw_file = "app/data/weekly/raw/weekly-2171.docx"   # 原始 Word 檔
    processed_file = "app/data/weekly/processed/weekly-2171.json"

    parser = WeeklyParser(raw_file)
    data = parser.parse()

    os.makedirs(os.path.dirname(processed_file), exist_ok=True)
    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已處理完成，輸出到 {processed_file}")
