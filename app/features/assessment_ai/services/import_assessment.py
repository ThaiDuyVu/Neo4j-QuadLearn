"""Validate Sơn's assessment payload before any graph write.

Payload is a dict with optional `questions` and `essays` lists. Each row belongs
to the supplied topic and grade. A failed row rejects the entire batch.
"""

from uuid import uuid4


def _text(value, field, row):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{row}: thiếu {field}")
    return value.strip()


def _optional_text(value, field, row):
    if not isinstance(value, str):
        raise ValueError(f"{row}: {field} phải là văn bản")
    return value.strip()


def prepare_batch(payload: dict, grade: int) -> dict:
    if grade not in (6, 7, 8, 9):
        raise ValueError("Lớp không hợp lệ")
    if not isinstance(payload, dict):
        raise ValueError("Payload phải là object")
    if any(key not in {"questions", "essays"} for key in payload):
        raise ValueError("Loại nội dung không được hỗ trợ")
    prepared = {"questions": [], "essays": []}
    for kind in prepared:
        rows = payload.get(kind, [])
        if not isinstance(rows, list):
            raise ValueError(f"{kind} phải là danh sách")
        for number, row in enumerate(rows, 1):
            label = f"{kind} dòng {row.get('_source_row', number) if isinstance(row, dict) else number}"
            if not isinstance(row, dict):
                raise ValueError(f"{label}: phải là object")
            if row.get("grade", grade) != grade:
                raise ValueError(f"{label}: sai lớp")
            status = row.get("status", "draft")
            if status != "draft":
                raise ValueError(f"{label}: nội dung import phải lưu Nháp")
            if kind == "questions":
                qtype = row.get("type")
                difficulty = row.get("difficulty")
                if qtype not in {"single", "multiple", "true_false"}:
                    raise ValueError(f"{label}: loại câu hỏi không hợp lệ")
                if difficulty not in {"recognize", "understand", "apply"}:
                    raise ValueError(f"{label}: mức độ không hợp lệ")
                options = row.get("options")
                if not isinstance(options, list) or len(options) < 2:
                    raise ValueError(f"{label}: cần ít nhất hai lựa chọn")
                clean_options = []
                for index, option in enumerate(options, 1):
                    option_label = f"options dòng {option.get('_source_row', index) if isinstance(option, dict) else index}"
                    if not isinstance(option, dict) or type(option.get("correct")) is not bool:
                        raise ValueError(f"{option_label}: correct phải là boolean")
                    clean_options.append({"id": f"option:{uuid4()}",
                                          "text_vi": _text(option.get("text_vi"), "nội dung đáp án", option_label),
                                          "correct": option["correct"]})
                correct_count = sum(option["correct"] for option in clean_options)
                if (correct_count < 1 or correct_count == len(clean_options)
                        or (qtype != "multiple" and correct_count != 1)
                        or (qtype == "true_false" and len(clean_options) != 2)):
                    raise ValueError(f"{label}: số đáp án đúng không hợp lệ")
                prepared[kind].append({
                    "id": f"question:{uuid4()}", "grade": grade,
                    "type": qtype, "difficulty": difficulty, "status": status,
                    "text_vi": _text(row.get("text_vi"), "câu hỏi", label),
                    "explanation_vi": _text(row.get("explanation_vi"), "giải thích", label),
                    "image_url": _optional_text(row.get("image_url", ""), "hình", label),
                    "options": clean_options,
                })
            else:
                essay_kind = row.get("kind", "calculation")
                if essay_kind not in {"calculation", "proof", "application"}:
                    raise ValueError(f"{label}: loại tự luận không hợp lệ")
                if grade == 6 and essay_kind == "proof":
                    raise ValueError(f"{label}: lớp 6 không có bài chứng minh")
                hints = row.get("hints", [])
                if not isinstance(hints, list):
                    raise ValueError(f"{label}: hints phải là danh sách")
                assumptions = row.get("assumptions_vi", "")
                conclusion = row.get("conclusion_vi", "")
                if not isinstance(assumptions, str) or not isinstance(conclusion, str):
                    raise ValueError(f"{label}: giả thiết/kết luận phải là văn bản")
                clean_hints = [{"id": f"hint:{uuid4()}", "order": index,
                                "text_vi": _text(hint.get("text_vi") if isinstance(hint, dict) else None,
                                                 "gợi ý", f"hints dòng {hint.get('_source_row', index) if isinstance(hint, dict) else index}"),
                                "image_url": _optional_text(hint.get("image_url", ""), "hình gợi ý", label)}
                               for index, hint in enumerate(hints, 1)]
                prepared[kind].append({
                    "id": f"essay:{uuid4()}", "grade": grade, "kind": essay_kind,
                    "status": status,
                    "prompt_vi": _text(row.get("prompt_vi"), "đề", label),
                    "assumptions_vi": assumptions.strip(),
                    "conclusion_vi": conclusion.strip(),
                    "solution_vi": _text(row.get("solution_vi"), "lời giải", label),
                    "image_url": _optional_text(row.get("image_url", ""), "hình", label),
                    "hints": clean_hints,
                })
    if not prepared["questions"] and not prepared["essays"]:
        raise ValueError("Batch rỗng")
    return prepared


class AssessmentImportService:
    def __init__(self, repository):
        self.repository = repository

    def import_batch(self, topic_id: str, grade: int, payload: dict) -> dict:
        if not topic_id:
            raise ValueError("Thiếu topic_id")
        prepared = prepare_batch(payload, grade)
        self.repository.import_batch(topic_id, grade, prepared)
        return {kind: len(rows) for kind, rows in prepared.items()}

    def import_xlsx(self, topic_id: str, grade: int, data: bytes) -> dict:
        from .import_xlsx import workbook_payload

        return self.import_batch(topic_id, grade, workbook_payload(data))

    def preview(self, topic_id: str) -> dict[str, list[dict]]:
        if not topic_id:
            raise ValueError("Thiếu topic_id")
        return self.repository.preview_assessment(topic_id)
