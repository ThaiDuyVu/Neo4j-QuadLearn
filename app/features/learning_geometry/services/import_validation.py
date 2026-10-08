"""Service for validating lesson import JSON/Excel payloads."""

from typing import Dict, Any, List
from app.features.learning_geometry.models.content import ImportValidationReport


class ImportValidationService:
    """Validates lesson data structure, grade ranges, bilingual requirements, and prerequisites."""

    ALLOWED_GRADES = {6, 7, 8, 9}

    def validate_lessons_payload(self, payload: Dict[str, Any]) -> ImportValidationReport:
        errors: List[str] = []
        warnings: List[str] = []
        lessons = payload.get("lessons", [])

        if not isinstance(lessons, list) or not lessons:
            return ImportValidationReport(
                is_valid=False,
                errors=["Payload không hợp lệ hoặc danh sách 'lessons' bị rỗng."],
                total_records=0
            )

        lesson_map = {l.get("id"): l for l in lessons if isinstance(l, dict) and "id" in l}

        for idx, lesson in enumerate(lessons, start=1):
            if not isinstance(lesson, dict):
                errors.append(f"Dòng {idx}: Bản ghi không phải là một object JSON hợp lệ.")
                continue

            lesson_id = lesson.get("id", f"Dòng_{idx}")

            # 1. Validation tiêu đề & nội dung tiếng Việt bắt buộc
            title = lesson.get("title", {})
            content = lesson.get("content", {})
            
            if isinstance(title, str):
                title = {"vi": title}
            if isinstance(content, str):
                content = {"vi": content}

            if not title.get("vi"):
                errors.append(f"Bài [{lesson_id}] (Dòng {idx}): Thiếu tiêu đề tiếng Việt ('title.vi').")
            if not content.get("vi"):
                errors.append(f"Bài [{lesson_id}] (Dòng {idx}): Thiếu nội dung tiếng Việt ('content.vi').")
            
            if not title.get("en") or not content.get("en"):
                warnings.append(f"Bài [{lesson_id}] (Dòng {idx}): Thiếu bản dịch tiếng Anh (sẽ dùng Fallback tiếng Việt).")

            # 2. Validation Grade
            grade = lesson.get("grade")
            if grade not in self.ALLOWED_GRADES:
                errors.append(f"Bài [{lesson_id}] (Dòng {idx}): Khối lớp '{grade}' không hợp lệ (Chỉ chấp nhận 6, 7, 8, 9).")

            # 3. Validation Prerequisites (REQUIRES)
            prereqs = lesson.get("prerequisites", [])
            if lesson_id in prereqs:
                errors.append(f"Bài [{lesson_id}] (Dòng {idx}): Bài học không thể tự phụ thuộc chính nó.")

            for p_id in prereqs:
                if p_id in lesson_map:
                    p_grade = lesson_map[p_id].get("grade")
                    if p_grade and grade and p_grade > grade:
                        errors.append(
                            f"Bài [{lesson_id}] (Lớp {grade}) không thể phụ thuộc bài [{p_id}] thuộc lớp cao hơn (Lớp {p_grade})."
                        )

        # 4. Kiểm tra chu trình phụ thuộc (Acyclic Check)
        cycle_errors = self._detect_cycles(lesson_map)
        errors.extend(cycle_errors)

        return ImportValidationReport(
            is_valid=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            total_records=len(lessons)
        )

    def _detect_cycles(self, lesson_map: Dict[str, Dict[str, Any]]) -> List[str]:
        errors = []
        visited = {}  # 0: Unvisited, 1: Visiting, 2: Visited

        def dfs(node_id: str, path: List[str]):
            visited[node_id] = 1
            path.append(node_id)

            lesson = lesson_map.get(node_id, {})
            for p_id in lesson.get("prerequisites", []):
                if p_id in lesson_map:
                    if visited.get(p_id) == 1:
                        cycle_str = " -> ".join(path[path.index(p_id):] + [p_id])
                        errors.append(f"Phát hiện chu trình phụ thuộc vòng (Acyclic Violation): {cycle_str}")
                    elif visited.get(p_id, 0) == 0:
                        dfs(p_id, path)

            path.pop()
            visited[node_id] = 2

        for l_id in lesson_map:
            if visited.get(l_id, 0) == 0:
                dfs(l_id, [])

        return errors