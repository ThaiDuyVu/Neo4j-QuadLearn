import unittest
from io import BytesIO
from xml.sax.saxutils import escape
from zipfile import ZipFile

from app.features.assessment_ai.services.import_assessment import AssessmentImportService
from app.features.assessment_ai.services.import_xlsx import workbook_payload


SHEETS = {
    "questions": [
        ["key", "grade", "type", "difficulty", "text_vi", "explanation_vi"],
        ["q1", "8", "single", "recognize", "Hình chữ nhật?", "Có bốn góc vuông"],
    ],
    "options": [
        ["question_key", "text_vi", "correct"],
        ["q1", "4", "true"], ["q1", "2", "false"],
    ],
    "essays": [
        ["key", "grade", "kind", "prompt_vi", "solution_vi"],
        ["e1", "8", "calculation", "Tính diện tích", "S = a × b"],
    ],
    "hints": [
        ["essay_key", "text_vi"], ["e1", "Dùng công thức diện tích"],
    ],
}


def workbook_bytes(sheets=SHEETS):
    stream = BytesIO()
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    office_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    names = list(sheets)
    with ZipFile(stream, "w") as archive:
        tabs = "".join(f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>'
                       for i, name in enumerate(names, 1))
        archive.writestr("xl/workbook.xml",
                         f'<workbook xmlns="{main_ns}" xmlns:r="{office_ns}"><sheets>{tabs}</sheets></workbook>')
        links = "".join(f'<Relationship Id="rId{i}" Target="worksheets/sheet{i}.xml"/>'
                        for i in range(1, len(names) + 1))
        archive.writestr("xl/_rels/workbook.xml.rels",
                         f'<Relationships xmlns="{package_ns}">{links}</Relationships>')
        for i, name in enumerate(names, 1):
            rows = []
            for row_index, values in enumerate(sheets[name], 1):
                cells = "".join(
                    f'<c r="{chr(65 + col)}{row_index}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
                    for col, value in enumerate(values))
                rows.append(f'<row r="{row_index}">{cells}</row>')
            archive.writestr(f"xl/worksheets/sheet{i}.xml",
                             f'<worksheet xmlns="{main_ns}"><sheetData>{"".join(rows)}</sheetData></worksheet>')
    return stream.getvalue()


class FakeRepository:
    def __init__(self):
        self.batch = None

    def import_batch(self, topic_id, grade, batch):
        self.batch = batch


class XlsxImportTests(unittest.TestCase):
    def test_valid_workbook_imports_question_and_essay(self):
        data = workbook_bytes()
        self.assertEqual(workbook_payload(data)["questions"][0]["options"][0]["correct"], True)
        repo = FakeRepository()
        counts = AssessmentImportService(repo).import_xlsx("topic:8:x", 8, data)
        self.assertEqual(counts, {"questions": 1, "essays": 1})
        self.assertEqual(repo.batch["essays"][0]["hints"][0]["order"], 1)

    def test_broken_link_rejects_entire_batch(self):
        sheets = {key: [row[:] for row in rows] for key, rows in SHEETS.items()}
        sheets["options"][1][0] = "missing"
        repo = FakeRepository()
        with self.assertRaises(ValueError):
            AssessmentImportService(repo).import_xlsx("topic:8:x", 8,
                                                       workbook_bytes(sheets))
        self.assertIsNone(repo.batch)

    def test_invalid_zip_is_rejected(self):
        with self.assertRaises(ValueError):
            workbook_payload(b"not an xlsx")


if __name__ == "__main__":
    unittest.main()
