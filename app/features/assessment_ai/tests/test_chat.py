import unittest
from datetime import datetime, timezone
from time import sleep

from app.features.assessment_ai.models.ai import AIRequest
from app.features.assessment_ai.services.chat import ChatService, QuotaExceeded
from app.shared.models.dto import LessonSummary


REQUEST = AIRequest("Giải thích hình chữ nhật", 8, "vi",
                    (LessonSummary("lesson:8:x", "Hình chữ nhật", 8, "topic:8:x"),))


class FakeQuota:
    def __init__(self, limit=10):
        self.used = 0
        self.pending = set()
        self.limit = limit
        self.records = []

    def remaining_quota(self, user_id, day, limit):
        return limit - self.used - len(self.pending)

    def reserve_quota(self, user_id, day, reservation_id, limit):
        if self.used + len(self.pending) >= limit:
            return False
        self.pending.add(reservation_id)
        return True

    def finish_quota(self, user_id, day, reservation_id, *, success, daily_limit,
                     record=None):
        self.pending.remove(reservation_id)
        self.used += int(success)
        if record:
            self.records.append(record)
        return daily_limit - self.used - len(self.pending)

    def chat_sessions(self, user_id):
        return [{"id": "chat:1"}]

    def chat_messages(self, user_id, session_id):
        return [{"id": "message:1", "role": "assistant"}]

    def delete_chat(self, user_id, session_id):
        self.deleted = (user_id, session_id)

    def chat_feedback(self, user_id, message_id, rating, report):
        self.feedback = (user_id, message_id, rating, report)


class Provider:
    def __init__(self, result="MOCK · Hình chữ nhật"):
        self.result = result
        self.calls = 0

    def respond(self, request):
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class SlowProvider:
    def respond(self, request):
        sleep(0.05)
        return "MOCK · Hình chữ nhật"


class ChatTests(unittest.TestCase):
    def test_success_consumes_one_credit_and_returns_sources(self):
        quota = FakeQuota()
        service = ChatService(quota, Provider(), daily_limit=2)
        reply = service.ask("user:1", REQUEST, datetime(2026, 10, 8, tzinfo=timezone.utc))
        self.assertEqual(reply.remaining, 1)
        self.assertEqual(reply.source_ids, ("lesson:8:x",))
        self.assertTrue(reply.session_id.startswith("chat:"))
        self.assertEqual((quota.used, quota.pending), (1, set()))
        self.assertEqual(quota.records[0]["sources"], ["lesson:8:x"])

    def test_followup_reuses_session_and_charges_one_credit(self):
        quota = FakeQuota()
        service = ChatService(quota, Provider())
        first = service.ask("user:1", REQUEST)
        followup = service.ask("user:1", REQUEST, session_id=first.session_id)
        self.assertEqual(followup.session_id, first.session_id)
        self.assertEqual(quota.used, 2)
        self.assertFalse(quota.records[0]["reuse_session"])
        self.assertTrue(quota.records[1]["reuse_session"])

    def test_invalid_followup_id_is_rejected_before_quota(self):
        quota = FakeQuota()
        provider = Provider()
        with self.assertRaises(ValueError):
            ChatService(quota, provider).ask("user:1", REQUEST, session_id="other:1")
        self.assertEqual((quota.used, provider.calls), (0, 0))

    def test_provider_error_and_timeout_refund(self):
        for provider, clock in ((Provider(RuntimeError("offline")), lambda: 0),
                                (Provider(), iter((0, 31)).__next__),
                                (Provider("ma túy"), lambda: 0)):
            quota = FakeQuota()
            service = ChatService(quota, provider, timeout_seconds=30, clock=clock)
            with self.assertRaises((RuntimeError, TimeoutError, ValueError)):
                service.ask("user:1", REQUEST)
            self.assertEqual((quota.used, quota.pending), (0, set()))

    def test_hard_timeout_returns_before_provider_finishes_and_refunds(self):
        quota = FakeQuota()
        service = ChatService(quota, SlowProvider(), timeout_seconds=0.01)
        with self.assertRaisesRegex(TimeoutError, "quá thời gian"):
            service.ask("user:1", REQUEST)
        self.assertEqual((quota.used, quota.pending), (0, set()))

    def test_quota_blocks_and_scope_rejection_does_not_reserve(self):
        quota = FakeQuota(limit=1)
        service = ChatService(quota, Provider(), daily_limit=1)
        service.ask("user:1", REQUEST)
        with self.assertRaises(QuotaExceeded):
            service.ask("user:1", REQUEST)
        self.assertEqual(quota.used, 1)
        other = FakeQuota()
        provider = Provider()
        with self.assertRaises(ValueError):
            ChatService(other, provider).ask("user:1", AIRequest("Bóng đá", 8, "vi", REQUEST.context))
        self.assertEqual((other.used, other.pending, provider.calls), (0, set(), 0))

    def test_history_feedback_and_delete_validate_ownership_inputs(self):
        repo = FakeQuota()
        chat = ChatService(repo, Provider())
        self.assertEqual(chat.sessions("user:1")[0]["id"], "chat:1")
        self.assertEqual(chat.messages("user:1", "chat:1")[0]["id"], "message:1")
        chat.feedback("user:1", "message:1", "helpful", True)
        self.assertEqual(repo.feedback, ("user:1", "message:1", "helpful", True))
        chat.delete_session("user:1", "chat:1")
        self.assertEqual(repo.deleted, ("user:1", "chat:1"))
        with self.assertRaises(ValueError):
            chat.feedback("user:1", "message:1", "neutral")

    def test_naive_time_is_rejected_before_quota(self):
        repo = FakeQuota()
        chat = ChatService(repo, Provider())
        with self.assertRaises(ValueError):
            chat.ask("user:1", REQUEST, datetime(2026, 10, 8))
        self.assertEqual(repo.pending, set())


if __name__ == "__main__":
    unittest.main()
