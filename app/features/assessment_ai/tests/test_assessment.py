import pytest
from app.features.assessment_ai.services.assessment import score
from app.features.assessment_ai.services.mock_ai import MockAIProvider
from app.features.assessment_ai.models.ai import AIRequest
from app.shared.models.dto import LessonSummary

@pytest.mark.parametrize("correct,total,expected", [(0,5,0),(3,5,6),(5,5,10),(1,3,3.33)])
def test_score(correct,total,expected): assert score(correct,total) == expected

@pytest.mark.parametrize("correct,total", [(0,0),(-1,5),(6,5)])
def test_invalid_score(correct,total):
    with pytest.raises(ValueError): score(correct,total)

def test_mock_has_label_and_context_not_identity():
    context = (LessonSummary("lesson:8:x", "Rectangle", 8, "topic:8:x"),)
    reply = MockAIProvider().respond(AIRequest("Why?",8,"vi",context))
    assert "MOCK" in reply and "Không phải LLM" in reply and "Rectangle" in reply

@pytest.mark.parametrize("grade,language", [(5,"vi"),(8,"fr")])
def test_mock_rejects_invalid_context(grade,language):
    with pytest.raises(ValueError): MockAIProvider().respond(AIRequest("?",grade,language,()))
