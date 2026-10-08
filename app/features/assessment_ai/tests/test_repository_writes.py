import unittest

from app.features.assessment_ai.models.quiz import AnswerResult, AttemptResult
from app.features.assessment_ai.repositories.assessment import AssessmentRepository


class Result:
    def __init__(self, row=None):
        self.row = row

    def single(self):
        return self.row

    def consume(self):
        return None


class Transaction:
    def __init__(self, valid=True):
        self.calls = []
        self.valid = valid

    def run(self, query, **params):
        self.calls.append((query, params))
        if "AS user_count" in query:
            return Result({"user_count": 1, "found": ["question:1"]})
        if "RETURN count(u) AS found" in query or "RETURN count(t) AS found" in query:
            return Result({"found": 1})
        if "a.selections_json AS selections_json" in query:
            return Result({"status": "draft", "mode": "test",
                           "question_ids": ["question:1"],
                           "selections_json": '{"question:1": ["option:a"]}'})
        if "AS available" in query:
            return Result({"available": ["option:a", "option:b"] if self.valid else [],
                           "correct_ids": ["option:a"]})
        return Result()


class Session:
    def __init__(self, tx):
        self.tx = tx
        self.write_calls = 0

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute_write(self, callback):
        self.write_calls += 1
        return callback(self.tx)


class Driver:
    def __init__(self, tx):
        self.active_session = Session(tx)

    def session(self, **kwargs):
        return self.active_session


class Database:
    database = "neo4j"

    def __init__(self, tx):
        self.driver = Driver(tx)


RESULT = AttemptResult(
    "attempt:test", "topic:8:x", 10.0,
    (AnswerResult("question:1", ("option:a",), True, ("option:a",), "Because"),),
    "2026-01-01T00:00:00+00:00", "2026-01-01T00:01:00+00:00",
)


class RepositoryWriteTests(unittest.TestCase):
    def test_followup_chat_checks_owner_and_lesson_before_writing_messages(self):
        class QuotaTransaction(Transaction):
            def __init__(self, lessons):
                super().__init__()
                self.lessons = lessons

            def run(self, query, **params):
                self.calls.append((query, params))
                if "RETURN q.id AS id" in query:
                    return Result({"id": "quota:1"})
                if "RETURN q.used AS used" in query:
                    return Result({"used": 1, "pending": 0})
                if "RETURN lessons" in query:
                    return Result({"lessons": self.lessons})
                return Result()

        record = {"reuse_session": True, "session_id": "chat:1",
                  "lesson_id": "lesson:1", "question_id": "message:q",
                  "answer_id": "message:a", "question": "Hình chữ nhật?",
                  "answer": "MOCK", "provider": "mock", "sources": ["lesson:1"]}
        accepted = QuotaTransaction(["lesson:1"])
        AssessmentRepository(Database(accepted)).finish_quota(
            "user:1", "2026-10-08", "reservation:1", success=True,
            daily_limit=10, record=record)
        self.assertTrue(any("CREATE (s)-[:HAS_MESSAGE]" in query
                            for query, _ in accepted.calls))
        rejected = QuotaTransaction(["lesson:other"])
        with self.assertRaises(ValueError):
            AssessmentRepository(Database(rejected)).finish_quota(
                "user:1", "2026-10-08", "reservation:1", success=True,
                daily_limit=10, record=record)
        self.assertFalse(any("CREATE (s)-[:HAS_MESSAGE]" in query
                             for query, _ in rejected.calls))

    def test_essay_review_persists_written_answer_in_one_transaction(self):
        class EssayTransaction(Transaction):
            def run(self, query, **params):
                self.calls.append((query, params))
                if "AS hint_count" in query:
                    return Result({"found": 1, "hint_count": 2})
                return Result()

        tx = EssayTransaction()
        db = Database(tx)
        repository = AssessmentRepository(db)
        repository._review_schema_ready = True
        repository.save_essay_review(
            "user:1", "essay:1", "essay-review:1", "understood", 1,
            "2026-01-01T00:00:00+00:00", "S = a × b")
        self.assertEqual(db.driver.active_session.write_calls, 1)
        query, params = tx.calls[-1]
        self.assertIn("answer_text:$answer_text", query)
        self.assertEqual(params["answer_text"], "S = a × b")

    def test_attempt_and_answer_share_one_transaction(self):
        tx = Transaction()
        db = Database(tx)
        AssessmentRepository(db).save_attempt("user:1", RESULT)
        self.assertEqual(db.driver.active_session.write_calls, 1)
        queries = [query for query, _ in tx.calls]
        self.assertEqual(sum("CREATE (a:Attempt" in query for query in queries), 1)
        self.assertEqual(sum("AttemptAnswer" in query for query in queries), 1)
        self.assertTrue(any("User {id:$user_id}" in query for query in queries))
        self.assertTrue(all("demo:coalesce" in query for query in queries
                            if "CREATE (a:Attempt" in query or "AttemptAnswer" in query))

    def test_stale_option_aborts_before_attempt_create(self):
        tx = Transaction(valid=False)
        with self.assertRaises(ValueError):
            AssessmentRepository(Database(tx)).save_attempt("user:1", RESULT)
        self.assertFalse(any("CREATE (a:Attempt" in query for query, _ in tx.calls))

    def test_import_rows_share_one_transaction(self):
        tx = Transaction()
        db = Database(tx)
        AssessmentRepository(db).import_batch("topic:8:x", 8,
                                              {"questions": [], "essays": []})
        self.assertEqual(db.driver.active_session.write_calls, 1)
        self.assertEqual(sum("CREATE (t)-[:HAS_" in query for query, _ in tx.calls), 2)
        self.assertTrue(all("demo:coalesce" in query for query, _ in tx.calls
                            if "CREATE (t)-[:HAS_" in query))

    def test_start_and_complete_test_do_not_create_option_nodes(self):
        tx = Transaction()
        db = Database(tx)
        repository = AssessmentRepository(db)
        repository.start_test("user:1", 8, "topic:8:x", "attempt:test",
                              ["question:1"], {"question:1": ["option:a", "option:b"]},
                              RESULT.started_at, 600)
        self.assertEqual(db.driver.active_session.write_calls, 1)
        repository.complete_test("user:1", RESULT)
        self.assertEqual(db.driver.active_session.write_calls, 2)
        queries = [query for query, _ in tx.calls]
        self.assertFalse(any("CREATE (x)-[:SELECTED]->(:Option" in query for query in queries))
        self.assertTrue(any("MATCH (q)-[:HAS_OPTION]->(o:Option" in query
                            for query in queries))


if __name__ == "__main__":
    unittest.main()
