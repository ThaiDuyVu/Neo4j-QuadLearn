import unittest
import json
from pathlib import Path

from app.features.assessment_ai.services.import_assessment import (
    AssessmentImportService, prepare_batch,
)
from app.features.assessment_ai.services.import_xlsx import workbook_payload
from app.features.assessment_ai.services.assessment import AssessmentService


QUESTION = {"grade": 8, "type": "single", "difficulty": "recognize",
            "text_vi": "Có mấy góc vuông?", "explanation_vi": "Có bốn.",
            "options": [{"text_vi": "4", "correct": True},
                        {"text_vi": "2", "correct": False}]}
ESSAY = {"grade": 8, "kind": "calculation", "prompt_vi": "Tính diện tích",
         "solution_vi": "S = a × b", "hints": [{"text_vi": "Dùng công thức diện tích"}]}


class FakeRepository:
    def __init__(self):
        self.calls = []

    def import_batch(self, topic_id, grade, batch):
        self.calls.append((topic_id, grade, batch))

    def preview_assessment(self, topic_id):
        return {"questions": [{"id": "question:1", "status": "draft"}],
                "essays": []}


class ImportTests(unittest.TestCase):
    def test_shipped_json_template_validates(self):
        path = Path(__file__).parents[1] / "examples" / "assessment_import.json"
        batch = prepare_batch(json.loads(path.read_text(encoding="utf-8")), 8)
        self.assertEqual((len(batch["questions"]), len(batch["essays"])), (1, 1))

    def test_shipped_xlsx_template_validates(self):
        path = Path(__file__).parents[1] / "examples" / "assessment_import.xlsx"
        batch = prepare_batch(workbook_payload(path.read_bytes()), 8)
        self.assertEqual((len(batch["questions"]), len(batch["essays"])), (1, 1))

    def test_valid_batch_prepares_draft_and_unique_ids(self):
        batch = prepare_batch({"questions": [QUESTION, QUESTION], "essays": [ESSAY]}, 8)
        self.assertEqual(len({q["id"] for q in batch["questions"]}), 2)
        self.assertEqual(batch["questions"][0]["status"], "draft")
        self.assertEqual(batch["essays"][0]["hints"][0]["order"], 1)
        repo = FakeRepository()
        result = AssessmentImportService(repo).import_batch("topic:8:x", 8,
                                                              {"questions": [QUESTION]})
        self.assertEqual(result, {"questions": 1, "essays": 0})
        self.assertEqual(len(repo.calls), 1)

    def test_invalid_batch_does_not_call_writer(self):
        repo = FakeRepository()
        bad = dict(QUESTION, options=[{"text_vi": "4", "correct": True},
                                           {"text_vi": "2", "correct": True}])
        with self.assertRaises(ValueError):
            AssessmentImportService(repo).import_batch("topic:8:x", 8,
                                                         {"questions": [bad]})
        self.assertEqual(repo.calls, [])

    def test_grade_six_proof_rejected(self):
        with self.assertRaises(ValueError):
            prepare_batch({"essays": [dict(ESSAY, grade=6, kind="proof")]}, 6)

    def test_import_cannot_bypass_draft_review(self):
        with self.assertRaisesRegex(ValueError, "Nháp"):
            prepare_batch({"questions": [dict(QUESTION, status="published")]}, 8)

    def test_preview_returns_assessment_items(self):
        result = AssessmentImportService(FakeRepository()).preview("topic:8:x")
        self.assertEqual(result["questions"][0]["status"], "draft")

    def test_composed_service_exposes_admin_import_contract(self):
        repo = FakeRepository()
        class AdminIdentity:
            def require_user(self, user_id=None, admin=False):
                return object()  # Fake admin đã được xác thực trong test import riêng.
        service = AssessmentService(repo, identity=AdminIdentity())
        result = service.import_assessment_batch("topic:8:x", 8,
                                                 {"questions": [QUESTION]})
        self.assertEqual(result, {"questions": 1, "essays": 0})
        self.assertEqual(len(repo.calls), 1)
        workbook = (Path(__file__).parents[1] / "examples" /
                    "assessment_import.xlsx").read_bytes()
        self.assertEqual(service.import_assessment_xlsx("topic:8:x", 8, workbook),
                         {"questions": 1, "essays": 1})
        self.assertEqual(service.preview_assessment("topic:8:x")["questions"][0]["status"],
                         "draft")


if __name__ == "__main__":
    unittest.main()
