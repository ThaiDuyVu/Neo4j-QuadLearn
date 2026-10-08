"""AI request orchestration with a transactional daily quota reservation."""

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from datetime import datetime, timedelta, timezone, tzinfo
from time import monotonic, time
from uuid import uuid4

from ..models.ai import AIProvider, AIRequest
from .ai_safety import ScreenedAIProvider, screen_request


@dataclass(frozen=True)
class ChatReply:
    text: str
    remaining: int
    source_ids: tuple[str, ...]
    session_id: str


class QuotaExceeded(ValueError):
    pass


class ChatService:
    def __init__(self, repository, provider: AIProvider, *, daily_limit: int = 10,
                 timeout_seconds: float = 30,
                 day_timezone: tzinfo = timezone(timedelta(hours=7)),
                 clock=monotonic):
        if daily_limit <= 0 or timeout_seconds <= 0:
            raise ValueError("Hạn mức và thời gian phải dương")
        self.repository = repository
        self.provider = ScreenedAIProvider(provider)
        self.daily_limit = daily_limit
        self.timeout_seconds = timeout_seconds
        self.timezone = day_timezone
        self.clock = clock

    def remaining(self, user_id: str, now: datetime | None = None) -> int:
        if not user_id:
            raise ValueError("Thiếu người học")
        if now is not None and now.tzinfo is None:
            raise ValueError("Thời gian phải có múi giờ")
        day = (now or datetime.now(self.timezone)).astimezone(self.timezone).date().isoformat()
        return self.repository.remaining_quota(user_id, day, self.daily_limit)

    def ask(self, user_id: str, request: AIRequest,
            now: datetime | None = None, session_id: str | None = None) -> ChatReply:
        if not user_id:
            raise ValueError("Thiếu người học")
        if session_id is not None and (not isinstance(session_id, str)
                                       or not session_id.startswith("chat:")
                                       or len(session_id) > 128):
            raise ValueError("Phiên chat không hợp lệ")
        if now is not None and now.tzinfo is None:
            raise ValueError("Thời gian phải có múi giờ")
        screen_request(request)
        day = (now or datetime.now(self.timezone)).astimezone(self.timezone).date().isoformat()
        reservation_id = f"{int(time())}:{uuid4()}"
        if not self.repository.reserve_quota(user_id, day, reservation_id, self.daily_limit):
            raise QuotaExceeded("Đã hết lượt hỏi AI hôm nay")
        started = self.clock()
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="assessment-ai")
        future = executor.submit(self.provider.respond, request)
        try:
            text = future.result(timeout=self.timeout_seconds)
            if self.clock() - started > self.timeout_seconds:
                raise TimeoutError("AI trả lời quá thời gian cho phép")
        except FutureTimeout as exc:
            future.cancel()
            self.repository.finish_quota(user_id, day, reservation_id,
                                         success=False, daily_limit=self.daily_limit)
            raise TimeoutError("AI trả lời quá thời gian cho phép") from exc
        except Exception:
            self.repository.finish_quota(user_id, day, reservation_id,
                                         success=False, daily_limit=self.daily_limit)
            raise
        finally:
            executor.shutdown(wait=False, cancel_futures=True)
        saved_session_id = session_id or f"chat:{uuid4()}"
        record = {"session_id": saved_session_id,
                  "reuse_session": session_id is not None,
                  "question_id": f"message:{uuid4()}",
                  "answer_id": f"message:{uuid4()}",
                  "question": request.question.strip(), "answer": text,
                  "lesson_id": request.lesson_id,
                  "sources": [item.id for item in request.context],
                  "provider": type(self.provider.provider).__name__.removesuffix("Provider").lower()}
        remaining = self.repository.finish_quota(user_id, day, reservation_id,
                                                 success=True, daily_limit=self.daily_limit,
                                                 record=record)
        return ChatReply(text, remaining, tuple(item.id for item in request.context),
                         saved_session_id)

    def sessions(self, user_id: str) -> list[dict]:
        if not user_id:
            raise ValueError("Thiếu người học")
        return self.repository.chat_sessions(user_id)

    def messages(self, user_id: str, session_id: str) -> list[dict]:
        if not user_id or not session_id:
            raise ValueError("Thiếu người học hoặc phiên chat")
        return self.repository.chat_messages(user_id, session_id)

    def delete_session(self, user_id: str, session_id: str) -> None:
        if not user_id or not session_id:
            raise ValueError("Thiếu người học hoặc phiên chat")
        self.repository.delete_chat(user_id, session_id)

    def feedback(self, user_id: str, message_id: str, rating: str,
                 report: bool = False) -> None:
        if rating not in {"helpful", "unhelpful"} or type(report) is not bool:
            raise ValueError("Đánh giá phản hồi không hợp lệ")
        self.repository.chat_feedback(user_id, message_id, rating, report)
