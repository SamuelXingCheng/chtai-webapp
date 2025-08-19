# weekly_parser.py
import json
import os
from docx import Document

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
        for para in self.doc.paragraphs[start_index:]:
            text = para.text.strip()
            if not text:
                continue
            style = para.style.name

            print(f"[{style}] {text[:50]}...")  # Debug

            if style == "Heading 2":
                self._new_section(text)
            elif style == "Heading 3":
                self._add_subtitle(text)
            elif style == "Normal":
                self._add_content(text)

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
