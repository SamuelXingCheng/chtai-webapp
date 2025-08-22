# weekly_parser.py
import json
import os
import io
from docx import Document
from PIL import Image
import re

class WeeklyParser:
    def __init__(self, file_path: str, image_dir: str):
        self.doc = Document(file_path)
        self.sections = []
        self.current_section = None
        self.image_count = 0
        self.image_dir = image_dir
        os.makedirs(self.image_dir, exist_ok=True)

    # ---------- 工具方法 ----------
    def _commit_section(self):
        if self.current_section:
            self.sections.append(self.current_section)
            self.current_section = None

    def _new_section(self, title: str):
        self._commit_section()
        self.current_section = {
            "type": "text",
            "title": title,
            "subtitle": "",
            "category": "truth",
            "content": "",
            "images": []
        }

    def _add_subtitle(self, subtitle: str):
        if self.current_section:
            self.current_section["subtitle"] = subtitle

    def _add_content(self, text: str):
        if self.current_section:
            if self.current_section["content"]:
                self.current_section["content"] += "\n" + text
            else:
                self.current_section["content"] = text

    def _add_image(self, image_bytes):
        """單純依序存圖片，不依賴 section"""
        self.image_count += 1
        try:
            image = Image.open(io.BytesIO(image_bytes))
            ext = image.format.lower() if image.format else "png"
            filename = f"{self.image_count}.{ext}"
            filepath = os.path.join(self.image_dir, filename)

            os.makedirs(self.image_dir, exist_ok=True)
            image.save(filepath)

            print(f"✅ Saved image {filepath}")
            return filename

        except Exception as e:
            print(f"❌ 存圖片失敗: {e}")
            return None

    def _extract_images_from_para(self, para):
        """解析段落中的圖片，直接存檔並記錄到 section"""
        for run in para.runs:
            blips = run._element.xpath('.//a:blip')
            for blip in blips:
                rId = blip.attrib.get(
                    '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'
                )
                if rId and rId in self.doc.part.related_parts:
                    image_part = self.doc.part.related_parts[rId]
                    filename = self._add_image(image_part.blob)
                    if filename and self.current_section is not None:
                        self.current_section["images"].append(filename)

    def _parse_intro(self, paragraphs):
        section = {
            "type": "text",
            "title": "開頭的話",
            "subtitle": "",
            "category": "truth",
            "content": "",
            "images": []
        }
        self.current_section = section

        subtitles = []
        content_lines = []

        for para in paragraphs:
            self._extract_images_from_para(para)
            text = para.text.strip()
            if not text:
                continue
            style = para.style.name
            if style == "Normal":
                if len(subtitles) < 2:
                    subtitles.append(text)
                else:
                    content_lines.append(text)

        section["subtitle"] = " ".join(subtitles)
        section["content"] = "\n".join(content_lines)
        self._commit_section()
        return section

    def _parse_progress_section(self, title, paragraphs, tables):
        self._new_section(title)
        section = self.current_section

        content_lines = []

        def extract_from_table(table, is_root=False):
            lines = []
            for row_idx, row in enumerate(table.rows):
                row_texts = [p.text.strip() for cell in row.cells for p in cell.paragraphs if p.text.strip()]
                if is_root and row_idx == 0 and row_texts and not section["subtitle"]:
                    section["subtitle"] = " ".join(row_texts)
                else:
                    if row_texts:
                        lines.append("".join(row_texts))
                for cell in row.cells:
                    for subtable in cell.tables:
                        lines.extend(extract_from_table(subtable))
            return lines

        for para in paragraphs:
            self._extract_images_from_para(para)

        for table in tables:
            lines = extract_from_table(table, is_root=True)
            content_lines.extend(lines)

        if "本週晨興進度申言主題" in title:
            normalized_lines = []
            big_text = "\n".join(content_lines)
            big_text = re.sub(
                r'([０-９]{1,2})、',
                lambda m: str(int("".join(chr(ord(c) - 65248) for c in m.group(1)))) + "、",
                big_text
            )
            matches = re.findall(r'(\d{1,2}、.+?)(?=\d{1,2}、|$)', big_text, flags=re.S)
            for m in matches:
                normalized_lines.append(m.strip())
            section["content"] = "\n".join(normalized_lines)
        else:
            section["content"] = "\n".join(content_lines)

        self._commit_section()
        return section

    def _parse_general_expansion_section(self, title, paragraphs):
        """解析 全地開展"""
        self._new_section(title)
        section = self.current_section

        content_lines = []
        for para in paragraphs:
            self._extract_images_from_para(para)
            text = para.text.strip()
            if not text:
                continue
            content_lines.append(text)

        if content_lines:
            section["subtitle"] = content_lines[0]
            section["content"] = "\n".join(content_lines[1:])
        else:
            section["subtitle"] = ""
            section["content"] = ""

        section["category"] = "expansion"
        self._commit_section()
        return section


    def _parse_home_meeting_section(self, title, paragraphs):
        section = {
            "type": "text",
            "title": title,
            "subtitle": "",
            "category": "truth",
            "sections": [],
            "images": []
        }

        current_sub = None
        for para in paragraphs:
            self._extract_images_from_para(para)
            text = para.text.strip()
            if not text:
                continue
            style = para.style.name

            if not section["subtitle"] and style == "Normal":
                section["subtitle"] = text
                continue

            if style == "Normal" and re.match(r'^[一二三四五六七八九十]+、', text):
                if current_sub:
                    section["sections"].append(current_sub)
                current_sub = {"heading": text, "paragraphs": []}
                continue

            if style in ["Normal", "List Paragraph"]:
                if not current_sub:
                    current_sub = {"heading": "", "paragraphs": []}
                current_sub["paragraphs"].append(text)

        if current_sub:
            section["sections"].append(current_sub)

        return section

    # ---------- 主流程 ----------
    def parse(self):
        intro_paragraphs = []
        start_index = 0
        for i, para in enumerate(self.doc.paragraphs):
            if para.style.name == "Heading 2":
                start_index = i
                break
            intro_paragraphs.append(para)

        self._parse_intro(intro_paragraphs)

        i = start_index
        table_index = 0
        while i < len(self.doc.paragraphs):
            para = self.doc.paragraphs[i]
            self._extract_images_from_para(para)
            text = para.text.strip()
            style = para.style.name
            if not text:
                i += 1
                continue

            print(f"[{style}] {text[:50]}...")

            if style == "Heading 2":
                if "本週晨興進度申言主題" in text:
                    block = []
                    i += 1
                    while i < len(self.doc.paragraphs):
                        p = self.doc.paragraphs[i]
                        if p.style.name == "Heading 2":
                            i -= 1
                            break
                        if "第二頁" in p.text:
                            break
                        block.append(p)
                        i += 1
                    tables = []
                    for t in self.doc.tables[table_index:]:
                        first_cell_text = t.cell(0, 0).text.strip()
                        print(f"DEBUG 表格第一格: {first_cell_text}")
                        if "週週福音" in first_cell_text or "台中市召會週訊" in first_cell_text:
                            table_index += 1
                            continue
                        tables = [t]
                        table_index += 1
                        break
                    self._parse_progress_section(text, block, tables)
                else:
                    self._new_section(text)

            elif style == "Normal" and text.startswith("全地開展"):
                print("🔍 偵測到 Normal 形式的 全地開展 -> 進入 _parse_general_expansion_section")
                block = []
                i += 1
                while i < len(self.doc.paragraphs):
                    p = self.doc.paragraphs[i]
                    p_text = p.text.strip()
                    if "家聚會牧養材料" in p_text:
                        i -= 1
                        break
                    block.append(p)
                    i += 1
                self._parse_general_expansion_section(text, block)

            elif style == "Normal" and "家聚會牧養材料" in text:
                print("🔍 偵測到 Normal 形式的 家聚會牧養材料 -> 進入 _parse_home_meeting_section")
                block = []
                i += 1
                while i < len(self.doc.paragraphs):
                    p = self.doc.paragraphs[i]
                    p_text = p.text.strip()
                    if p.style.name == "Heading 2" or ("聖經學習單" in p_text):
                        i -= 1
                        break
                    block.append(p)
                    i += 1
                home_section = self._parse_home_meeting_section(text, block)
                self.sections.append(home_section)

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
    raw_file = "app/data/weekly/raw/weekly-2171.docx"
    processed_file = "app/data/weekly/processed/weekly-2171.json"
    image_dir = "app/data/weekly/images/weekly-2171"

    parser = WeeklyParser(raw_file, image_dir)
    data = parser.parse()

    os.makedirs(os.path.dirname(processed_file), exist_ok=True)
    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已處理完成，輸出到 {processed_file}")
