"""Deterministic first-pass guard for the mock/provider boundary.

This is a narrow ruleset, not a complete child-safety classifier. A real LLM
deployment still needs reviewed policies and a larger evaluation corpus.
"""

import unicodedata

from ..models.ai import AIRequest, AIProvider


TOPIC_TERMS = (
    "tu giac", "hinh", "goc", "canh", "duong cheo", "chu vi", "dien tich",
    "song song", "vuong goc", "chung minh", "rectangle", "square", "rhombus",
    "parallelogram", "trapezoid", "quadrilateral", "polygon", "angle",
    "diagonal", "perimeter", "area", "parallel", "perpendicular", "geometry",
)
UNSAFE_TERMS = (
    "tu tu", "giet nguoi", "ma tuy", "khieu dam", "bao luc", "suicide",
    "kill someone", "make a bomb", "porn", "sexual content", "drugs",
)


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in value if not unicodedata.combining(char)).replace("đ", "d")


def screen_request(request: AIRequest) -> None:
    if request.grade not in (6, 7, 8, 9) or request.language not in ("vi", "en"):
        raise ValueError("Lớp hoặc ngôn ngữ không hợp lệ")
    if request.purpose not in {"tutor", "assessment_hint"}:
        raise ValueError("Mục đích hỏi AI không hợp lệ")
    if not isinstance(request.question, str) or not 3 <= len(request.question.strip()) <= 1000:
        raise ValueError("Câu hỏi phải dài 3–1000 ký tự")
    question = _normalize(request.question)
    if any(term in question for term in UNSAFE_TERMS):
        raise ValueError("Nội dung không phù hợp lứa tuổi")
    context_terms = tuple(_normalize(item.title) for item in request.context)
    if not any(term in question for term in TOPIC_TERMS + context_terms if len(term) >= 3):
        raise ValueError("Chỉ hỗ trợ câu hỏi về hình học tứ giác")
    if any(item.grade > request.grade for item in request.context):
        raise ValueError("Ngữ cảnh vượt quá lớp của người học")
    if request.lesson_id and request.lesson_id not in {item.id for item in request.context}:
        raise ValueError("Bài học hiện tại không nằm trong ngữ cảnh")


class ScreenedAIProvider:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def respond(self, request: AIRequest) -> str:
        screen_request(request)
        reply = self.provider.respond(request)
        if not isinstance(reply, str) or not reply.strip():
            raise ValueError("Provider trả lời rỗng")
        if any(term in _normalize(reply) for term in UNSAFE_TERMS):
            raise ValueError("Phản hồi không phù hợp lứa tuổi")
        return reply
