"""Read the assessment portion of an .xlsx workbook without touching Sơn's importer."""

from io import BytesIO
from pathlib import PurePosixPath
from zipfile import BadZipFile, ZipFile
from xml.etree import ElementTree as ET


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}
MAX_FILE = 5_000_000
MAX_UNCOMPRESSED = 20_000_000


def _column(reference: str) -> int:
    letters = "".join(char for char in reference if char.isalpha()).upper()
    number = 0
    for char in letters:
        number = number * 26 + ord(char) - ord("A") + 1
    return number - 1


def _sheet_rows(archive: ZipFile, path: str, strings: list[str]) -> list[dict]:
    root = ET.fromstring(archive.read(path))
    rows = []
    for row in root.findall(".//m:sheetData/m:row", NS):
        cells = {}
        for cell in row.findall("m:c", NS):
            if cell.find("m:f", NS) is not None:
                raise ValueError(f"Ô {cell.get('r')} chứa công thức; cần giá trị tĩnh")
            index = _column(cell.get("r", ""))
            if index < 0:
                continue
            if cell.get("t") == "inlineStr":
                value = "".join(node.text or "" for node in cell.findall(".//m:t", NS))
            else:
                node = cell.find("m:v", NS)
                value = node.text if node is not None else ""
                if cell.get("t") == "s" and value:
                    value = strings[int(value)]
            cells[index] = value or ""
        if cells:
            rows.append((int(row.get("r", "0")), cells))
    if not rows:
        return []
    headers = {index: name.strip() for index, name in rows[0][1].items() if name.strip()}
    if len(set(headers.values())) != len(headers):
        raise ValueError("Tên cột Excel bị trùng")
    return [dict({"_row": number}, **{
        name: cells.get(index, "") for index, name in headers.items()
    }) for number, cells in rows[1:] if any(value.strip() for value in cells.values())]


def read_workbook(data: bytes) -> dict[str, list[dict]]:
    if not isinstance(data, bytes) or len(data) > MAX_FILE:
        raise ValueError("File Excel không hợp lệ hoặc quá 5 MB")
    try:
        with ZipFile(BytesIO(data)) as archive:
            if sum(info.file_size for info in archive.infolist()) > MAX_UNCOMPRESSED:
                raise ValueError("File Excel giải nén vượt giới hạn")
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            targets = {item.get("Id"): item.get("Target")
                       for item in relationships.findall("p:Relationship", NS)}
            try:
                shared = ET.fromstring(archive.read("xl/sharedStrings.xml"))
                strings = ["".join(node.text or "" for node in item.findall(".//m:t", NS))
                           for item in shared.findall("m:si", NS)]
            except KeyError:
                strings = []
            sheets = {}
            for sheet in workbook.findall(".//m:sheets/m:sheet", NS):
                name = sheet.get("name", "").lower()
                if name not in {"questions", "options", "essays", "hints"}:
                    continue
                target = targets.get(sheet.get(f"{{{NS['r']}}}id"))
                if not target:
                    raise ValueError(f"Sheet {name} thiếu liên kết")
                path = str(PurePosixPath("xl") / target.lstrip("/"))
                if target.startswith("/xl/") or target.startswith("xl/"):
                    path = target.lstrip("/")
                if ".." in PurePosixPath(path).parts:
                    raise ValueError("Đường dẫn sheet không hợp lệ")
                sheets[name] = _sheet_rows(archive, path, strings)
            return sheets
    except (BadZipFile, KeyError, ET.ParseError, IndexError) as exc:
        raise ValueError("File Excel .xlsx không hợp lệ") from exc


def _boolean(value: str, location: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"{location}: correct phải là true/false")


def _grade(value: str, location: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{location}: grade phải là số nguyên") from exc


def workbook_payload(data: bytes) -> dict:
    sheets = read_workbook(data)
    questions = []
    essays = []
    question_keys = {}
    essay_keys = {}
    for row in sheets.get("questions", []):
        location = f"questions dòng {row['_row']}"
        key = row.get("key", "").strip()
        if not key or key in question_keys:
            raise ValueError(f"{location}: key trống hoặc trùng")
        question_keys[key] = len(questions)
        questions.append({"_source_row": row["_row"],
                          "grade": _grade(row.get("grade"), location),
                          "status": row.get("status") or "draft",
                          "type": row.get("type"),
                          "difficulty": row.get("difficulty"),
                          "text_vi": row.get("text_vi"),
                          "explanation_vi": row.get("explanation_vi"),
                          "image_url": row.get("image_url", ""), "options": []})
    for row in sheets.get("options", []):
        location = f"options dòng {row['_row']}"
        key = row.get("question_key", "").strip()
        if key not in question_keys:
            raise ValueError(f"{location}: question_key không tồn tại")
        questions[question_keys[key]]["options"].append({
            "_source_row": row["_row"],
            "text_vi": row.get("text_vi"),
            "correct": _boolean(row.get("correct", ""), location)})
    for row in sheets.get("essays", []):
        location = f"essays dòng {row['_row']}"
        key = row.get("key", "").strip()
        if not key or key in essay_keys:
            raise ValueError(f"{location}: key trống hoặc trùng")
        essay_keys[key] = len(essays)
        essays.append({"_source_row": row["_row"],
                       "grade": _grade(row.get("grade"), location),
                       "status": row.get("status") or "draft",
                       "kind": row.get("kind") or "calculation",
                       "prompt_vi": row.get("prompt_vi"),
                       "assumptions_vi": row.get("assumptions_vi", ""),
                       "conclusion_vi": row.get("conclusion_vi", ""),
                       "solution_vi": row.get("solution_vi"),
                       "image_url": row.get("image_url", ""), "hints": []})
    for row in sheets.get("hints", []):
        location = f"hints dòng {row['_row']}"
        key = row.get("essay_key", "").strip()
        if key not in essay_keys:
            raise ValueError(f"{location}: essay_key không tồn tại")
        essays[essay_keys[key]]["hints"].append({
            "_source_row": row["_row"],
            "text_vi": row.get("text_vi"), "image_url": row.get("image_url", "")})
    return {"questions": questions, "essays": essays}
