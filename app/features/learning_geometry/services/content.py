# DOMAIN OWNER: SON · learning_geometry
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
class ContentService:
    def __init__(self, repository):
        self.repository = repository

    def lessons(self, grade: int):
        if grade not in (6, 7, 8, 9):
            raise ValueError("Lớp phải thuộc 6–9")
        return self.repository.lessons(grade)

    def prerequisites(self, lesson_id: str):
        return self.repository.prerequisites(lesson_id)

    def ai_context(self, lesson_id: str):
        return self.repository.ai_context(lesson_id)
