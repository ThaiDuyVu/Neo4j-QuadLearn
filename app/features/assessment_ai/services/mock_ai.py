# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
from ..models.ai import AIRequest

class MockAIProvider:
    """Phản hồi cố định để test contract, không suy luận và không gọi LLM."""
    def respond(self, request: AIRequest) -> str:
        if request.grade not in (6, 7, 8, 9) or request.language not in ("vi", "en"):
            raise ValueError("Ngữ cảnh lớp/ngôn ngữ không hợp lệ")
        prefix = "MOCK ONLY · No LLM" if request.language == "en" else "CHỈ LÀ MOCK · Không phải LLM"
        titles = ", ".join(item.title for item in request.context) or "(no context)"
        return f"{prefix} · Grade {request.grade}. Context: {titles}."
