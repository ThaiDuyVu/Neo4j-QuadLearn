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
        content = next((item.content for item in request.context if item.content), "")
        if request.purpose == "assessment_hint":
            if request.language == "en":
                return (f"{prefix} · Grade {request.grade}. Hint only: identify the given "
                        "facts, name one relevant property, and justify the next step yourself.")
            return (f"{prefix} · Lớp {request.grade}. Chỉ gợi mở: xác định giả thiết, "
                    "nêu một tính chất liên quan rồi tự giải thích bước tiếp theo.")
        if request.language == "vi":
            guide = ("Hãy quan sát hình và thử nêu tính chất em thấy."
                     if request.grade <= 7 else
                     "Hãy đối chiếu định nghĩa, giả thiết và kết luận trước khi lập luận.")
        else:
            guide = ("Look at the shape and describe what you notice."
                     if request.grade <= 7 else
                     "Compare the definition, assumptions, and conclusion before proving.")
        return f"{prefix} · Grade {request.grade}. Context: {titles}. {guide} {content}".strip()
