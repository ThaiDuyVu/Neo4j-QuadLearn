"""Translation and i18n fallback service."""

from typing import Tuple


class TranslationService:
    """Handles content translation fallbacks and UI label localized resolution."""

    @staticmethod
    def resolve_bilingual_content(content_vi: str, content_en: str | None, target_lang: str) -> Tuple[str, bool]:
        if target_lang == "en":
            if content_en and content_en.strip():
                return content_en, False
            return content_vi or "", True
        return content_vi or "", False

    @staticmethod
    def get_ui_label(key: str, lang: str = "vi") -> str:
        labels = {
            "btn_mark_completed": {"vi": "Đánh dấu đã học xong", "en": "Mark as Completed"},
            "btn_next_lesson": {"vi": "Bài tiếp theo", "en": "Next Lesson"},
            "btn_prev_lesson": {"vi": "Bài trước đó", "en": "Previous Lesson"},
            "fallback_notice": {
                "vi": "Nội dung chưa có bản tiếng Anh. Đang hiển thị bản tiếng Việt.",
                "en": "English content unavailable. Displaying Vietnamese version."
            }
        }
        return labels.get(key, {}).get(lang, key)