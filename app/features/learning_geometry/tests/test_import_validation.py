"""Unit tests for ImportValidationService without Neo4j DB dependency."""

import pytest
from app.features.learning_geometry.services.import_validation import ImportValidationService


@pytest.fixture
def validator():
    return ImportValidationService()


def test_valid_payload(validator):
    payload = {
        "lessons": [
            {
                "id": "LES_01",
                "grade": 8,
                "title": {"vi": "Hình bình hành"},
                "content": {"vi": "Nội dung hình bình hành"},
                "prerequisites": []
            }
        ]
    }
    report = validator.validate_lessons_payload(payload)
    assert report.is_valid is True
    assert len(report.errors) == 0


def test_invalid_grade_and_cyclic_dependency(validator):
    payload = {
        "lessons": [
            {
                "id": "LES_A",
                "grade": 5,
                "title": {"vi": "Bài A"},
                "content": {"vi": "Nội dung A"},
                "prerequisites": ["LES_B"]
            },
            {
                "id": "LES_B",
                "grade": 8,
                "title": {"vi": "Bài B"},
                "content": {"vi": "Nội dung B"},
                "prerequisites": ["LES_A"]
            }
        ]
    }
    report = validator.validate_lessons_payload(payload)
    assert report.is_valid is False
    assert any("không hợp lệ" in err for err in report.errors)
    assert any("Acyclic Violation" in err for err in report.errors)