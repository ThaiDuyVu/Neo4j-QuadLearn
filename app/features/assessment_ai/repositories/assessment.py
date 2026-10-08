# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
from app.shared.contracts.ports import QueryExecutor
from app.shared.models.dto import AttemptSummary
import json
from ..models.quiz import Question, Option, AttemptResult
from ..models.essay import EssayProblem, EssayHint, validate_essay
from time import time

QUESTION_QUERY = """
MATCH (t:Topic)-[:HAS_QUESTION]->(q:Question)
WHERE t.grade = $grade AND t.status = 'published' AND q.status = 'published'
  AND ($topic_id IS NULL OR t.id = $topic_id)
  AND ($difficulty IS NULL OR q.difficulty = $difficulty)
OPTIONAL MATCH (q)-[:HAS_OPTION]->(o:Option)
WITH t, q, o ORDER BY o.id
RETURN q.id AS id, t.id AS topic_id, q.grade AS grade,
       q.difficulty AS difficulty, q.type AS kind,
       coalesce(q.text_vi, '') AS text,
       coalesce(q.explanation_vi, '') AS explanation,
       coalesce(q.image_url, '') AS image_url,
       collect({id:o.id, text:coalesce(o.text_vi, ''), correct:o.correct}) AS options
ORDER BY t.id, q.id
"""

class AssessmentRepository:
    def __init__(self, db: QueryExecutor):
        self.db = db
        self._quota_schema_ready = False
        self._review_schema_ready = False

    def _ensure_review_schema(self) -> None:
        if self._review_schema_ready:
            return
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Essay review requires a Neo4j driver")
        with driver.session(database=self.db.database) as session:
            session.run("""
                CREATE CONSTRAINT essayreview_id IF NOT EXISTS
                FOR (n:EssayReview) REQUIRE n.id IS UNIQUE
            """).consume()
        self._review_schema_ready = True

    def _ensure_quota_schema(self) -> None:
        if self._quota_schema_ready:
            return
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("AI quota requires a Neo4j driver")
        with driver.session(database=self.db.database) as session:
            session.run("""
                CREATE CONSTRAINT aiquotaday_id IF NOT EXISTS
                FOR (n:AIQuotaDay) REQUIRE n.id IS UNIQUE
            """).consume()
        self._quota_schema_ready = True

    def remaining_quota(self, user_id: str, day: str, daily_limit: int) -> int:
        rows = self.db.read("""
            MATCH (u:User {id:$user_id})
            OPTIONAL MATCH (q:AIQuotaDay {id:$id, user_id:$user_id})
            RETURN coalesce(q.used,0) AS used,
                   size([rid IN coalesce(q.pending,[])
                         WHERE toInteger(split(rid,':')[0]) >= $cutoff]) AS pending
        """, id=f"ai-quota:{user_id}:{day}", user_id=user_id,
             cutoff=int(time()) - 60)
        if not rows:
            raise ValueError("Người học không tồn tại")
        row = rows[0]
        return max(0, daily_limit - row["used"] - row["pending"])

    def reserve_quota(self, user_id: str, day: str, reservation_id: str,
                      daily_limit: int) -> bool:
        self._ensure_quota_schema()
        quota_id = f"ai-quota:{user_id}:{day}"

        def write(tx):
            owner = tx.run("""
                MATCH (u:User {id:$user_id})
                MERGE (q:AIQuotaDay {id:$id})
                ON CREATE SET q.user_id=u.id, q.day=$day, q.used=0, q.pending=[],
                              q.demo=coalesce(u.demo,false)
                SET q.lock=coalesce(q.lock,0)+1
                RETURN q.user_id AS owner
            """, user_id=user_id, id=quota_id, day=day).single()
            if not owner or owner["owner"] != user_id:
                raise ValueError("Người học không tồn tại hoặc hạn mức không thuộc người học")
            tx.run("""
                MATCH (q:AIQuotaDay {id:$id})
                SET q.pending=[rid IN q.pending
                    WHERE toInteger(split(rid,':')[0]) >= $cutoff]
            """, id=quota_id, cutoff=int(time()) - 60).consume()
            reserved = tx.run("""
                MATCH (q:AIQuotaDay {id:$id})
                WHERE q.used + size(q.pending) < $limit
                  AND NOT ($reservation_id IN q.pending)
                SET q.pending=q.pending + $reservation_id
                RETURN q.id AS id
            """, id=quota_id, limit=daily_limit,
                reservation_id=reservation_id).single()
            return reserved is not None

        with self.db.driver.session(database=self.db.database) as session:
            return session.execute_write(write)

    def finish_quota(self, user_id: str, day: str, reservation_id: str,
                     *, success: bool, daily_limit: int, record: dict | None = None) -> int:
        quota_id = f"ai-quota:{user_id}:{day}"

        def write(tx):
            locked = tx.run("""
                MATCH (q:AIQuotaDay {id:$id, user_id:$user_id})
                SET q.lock=coalesce(q.lock,0)+1
                RETURN q.id AS id
            """, id=quota_id, user_id=user_id).single()
            if not locked:
                raise RuntimeError("Không tìm thấy hạn mức đã đặt trước")
            finished = tx.run("""
                MATCH (q:AIQuotaDay {id:$id, user_id:$user_id})
                WHERE $reservation_id IN q.pending
                SET q.pending=[rid IN q.pending WHERE rid <> $reservation_id],
                    q.used=q.used + CASE WHEN $success THEN 1 ELSE 0 END
                RETURN q.used AS used, size(q.pending) AS pending
            """, id=quota_id, user_id=user_id, reservation_id=reservation_id,
                success=success).single()
            if not finished:
                raise RuntimeError("Lượt hỏi đã được quyết toán")
            if success:
                if record is None:
                    raise ValueError("Thiếu hội thoại để lưu")
                if record.get("reuse_session"):
                    owned = tx.run("""
                        MATCH (:User {id:$user_id})-[:HAS_CHAT]->
                              (s:ChatSession {id:$session_id})
                        OPTIONAL MATCH (s)-[:CONTEXT_LESSON]->(lesson:Lesson)
                        WITH s, collect(lesson.id) AS lessons
                        SET s.updated_at=datetime()
                        RETURN lessons
                    """, user_id=user_id, session_id=record["session_id"]).single()
                    if (not owned or owned["lessons"] !=
                            ([record["lesson_id"]] if record["lesson_id"] else [])):
                        raise ValueError("Phiên chat không thuộc người học hoặc khác bài học")
                    tx.run("""
                        MATCH (u:User {id:$user_id})-[:HAS_CHAT]->
                              (s:ChatSession {id:$session_id})
                        CREATE (s)-[:HAS_MESSAGE]->(:ChatMessage {
                            id:$question_id, role:'user', content:$question,
                            created_at:datetime(), demo:coalesce(u.demo,false)})
                        CREATE (s)-[:HAS_MESSAGE]->(:ChatMessage {
                            id:$answer_id, role:'assistant', content:$answer,
                            provider:$provider, sources:$sources, created_at:datetime(),
                            demo:coalesce(u.demo,false)})
                    """, user_id=user_id, **record).consume()
                else:
                    tx.run("""
                        MATCH (u:User {id:$user_id})
                        OPTIONAL MATCH (lesson:Lesson {id:$lesson_id})
                        CREATE (u)-[:HAS_CHAT]->(s:ChatSession {
                            id:$session_id, created_at:datetime(),
                            updated_at:datetime(), demo:coalesce(u.demo,false)})
                        CREATE (s)-[:HAS_MESSAGE]->(:ChatMessage {
                            id:$question_id, role:'user', content:$question,
                            created_at:datetime(), demo:coalesce(u.demo,false)})
                        CREATE (s)-[:HAS_MESSAGE]->(:ChatMessage {
                            id:$answer_id, role:'assistant', content:$answer,
                            provider:$provider, sources:$sources, created_at:datetime(),
                            demo:coalesce(u.demo,false)})
                        FOREACH (_ IN CASE WHEN lesson IS NULL THEN [] ELSE [1] END |
                            CREATE (s)-[:CONTEXT_LESSON]->(lesson))
                    """, user_id=user_id, **record).consume()
            return max(0, daily_limit - finished["used"] - finished["pending"])

        with self.db.driver.session(database=self.db.database) as session:
            return session.execute_write(write)

    def chat_sessions(self, user_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:HAS_CHAT]->(s:ChatSession)
            OPTIONAL MATCH (s)-[:CONTEXT_LESSON]->(lesson:Lesson)
            RETURN s.id AS id, toString(s.created_at) AS created_at,
                   lesson.id AS lesson_id, lesson.title_vi AS lesson_title
            ORDER BY coalesce(s.updated_at,s.created_at) DESC, s.id
        """, user_id=user_id)

    def chat_messages(self, user_id: str, session_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:HAS_CHAT]->(:ChatSession {id:$session_id})
                  -[:HAS_MESSAGE]->(m:ChatMessage)
            RETURN m.id AS id, m.role AS role, m.content AS content,
                   coalesce(m.provider,'') AS provider,
                   coalesce(m.sources,[]) AS sources,
                   m.feedback AS feedback, coalesce(m.report,false) AS report,
                   toString(m.created_at) AS created_at
            ORDER BY m.created_at,
                     CASE WHEN m.role='user' THEN 0 ELSE 1 END, m.id
        """, user_id=user_id, session_id=session_id)

    def delete_chat(self, user_id: str, session_id: str) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Chat deletion requires a Neo4j driver")

        def write(tx):
            owned = tx.run("""
                MATCH (:User {id:$user_id})-[:HAS_CHAT]->(s:ChatSession {id:$session_id})
                RETURN s.id AS id
            """, user_id=user_id, session_id=session_id).single()
            if not owned:
                raise ValueError("Không tìm thấy phiên chat của người học")
            tx.run("""
                MATCH (:User {id:$user_id})-[:HAS_CHAT]->(s:ChatSession {id:$session_id})
                      -[:HAS_MESSAGE]->(m:ChatMessage)
                DETACH DELETE m
            """, user_id=user_id, session_id=session_id).consume()
            tx.run("""
                MATCH (:User {id:$user_id})-[:HAS_CHAT]->(s:ChatSession {id:$session_id})
                DETACH DELETE s
            """, user_id=user_id, session_id=session_id).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def chat_feedback(self, user_id: str, message_id: str, rating: str,
                      report: bool) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Chat feedback requires a Neo4j driver")

        def write(tx):
            updated = tx.run("""
                MATCH (:User {id:$user_id})-[:HAS_CHAT]->(:ChatSession)
                      -[:HAS_MESSAGE]->(m:ChatMessage {id:$message_id, role:'assistant'})
                SET m.feedback=$rating, m.report=$report
                RETURN m.id AS id
            """, user_id=user_id, message_id=message_id,
                rating=rating, report=report).single()
            if not updated:
                raise ValueError("Không tìm thấy câu trả lời AI của người học")

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def attempts(self, user_id: str):
        return [AttemptSummary(**r) for r in self.db.read("""
            MATCH (:User {id: $id})-[:ATTEMPTED]->(a:Attempt)-[:FOR_TOPIC]->(t:Topic)
            WHERE a.status='completed'
            RETURN a.id AS id, t.id AS topic_id, a.score AS score, a.status AS status
            ORDER BY a.started_at DESC, a.id
        """, id=user_id)]

    def attempt_history(self, user_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt)-[:FOR_TOPIC]->(t:Topic)
            WHERE a.status='completed'
            RETURN a.id AS id, t.id AS topic_id, t.name_vi AS topic,
                   t.grade AS grade,
                   a.score AS score, a.status AS status,
                   toString(a.started_at) AS started_at,
                   toString(a.finished_at) AS finished_at,
                   duration.inSeconds(a.started_at,a.finished_at).seconds AS duration_seconds
            ORDER BY a.started_at DESC, a.id
        """, user_id=user_id)

    @staticmethod
    def _question(row):
        return Question(row["id"], row["topic_id"], row["grade"], row["difficulty"],
                        row["kind"], row["text"], row["explanation"],
                        tuple(Option(**option) for option in row["options"] if option["id"]),
                        row["image_url"])

    def questions(self, grade: int, topic_id: str | None = None,
                  difficulty: str | None = None) -> list[Question]:
        return [self._question(row) for row in self.db.read(
            QUESTION_QUERY, grade=grade, topic_id=topic_id, difficulty=difficulty)]

    def questions_for_attempt(self, topic_id: str, ids: tuple[str, ...]) -> list[Question]:
        rows = self.db.read("""
            MATCH (t:Topic {id:$topic_id})-[:HAS_QUESTION]->(q:Question)
            WHERE t.status='published' AND q.status='published' AND q.id IN $ids
            OPTIONAL MATCH (q)-[:HAS_OPTION]->(o:Option)
            WITH t,q,o ORDER BY o.id
            RETURN q.id AS id, t.id AS topic_id, q.grade AS grade,
                   q.difficulty AS difficulty, q.type AS kind,
                   coalesce(q.text_vi,'') AS text,
                   coalesce(q.explanation_vi,'') AS explanation,
                   coalesce(q.image_url,'') AS image_url,
                   collect({id:o.id,text:coalesce(o.text_vi,''),correct:o.correct}) AS options
            ORDER BY q.id
        """, topic_id=topic_id, ids=list(ids))
        return [self._question(row) for row in rows]

    def placement_questions(self, grades: tuple[int, ...]) -> list[Question]:
        rows = self.db.read("""
            MATCH (t:Topic)-[:HAS_QUESTION]->(q:Question)
            WHERE t.status='published' AND q.status='published'
              AND q.grade IN $grades AND t.grade=q.grade
            OPTIONAL MATCH (q)-[:HAS_OPTION]->(o:Option)
            WITH t,q,o ORDER BY o.id
            RETURN q.id AS id, t.id AS topic_id, q.grade AS grade,
                   q.difficulty AS difficulty, q.type AS kind,
                   coalesce(q.text_vi,'') AS text,
                   coalesce(q.explanation_vi,'') AS explanation,
                   coalesce(q.image_url,'') AS image_url,
                   collect({id:o.id,text:coalesce(o.text_vi,''),correct:o.correct}) AS options
            ORDER BY q.grade, q.id
        """, grades=list(grades))
        return [self._question(row) for row in rows]

    def placement_questions_by_ids(self, ids: tuple[str, ...]) -> list[Question]:
        rows = self.db.read("""
            MATCH (t:Topic)-[:HAS_QUESTION]->(q:Question)
            WHERE t.status='published' AND q.status='published'
              AND q.id IN $ids AND t.grade=q.grade
            OPTIONAL MATCH (q)-[:HAS_OPTION]->(o:Option)
            WITH t,q,o ORDER BY o.id
            RETURN q.id AS id, t.id AS topic_id, q.grade AS grade,
                   q.difficulty AS difficulty, q.type AS kind,
                   coalesce(q.text_vi,'') AS text,
                   coalesce(q.explanation_vi,'') AS explanation,
                   coalesce(q.image_url,'') AS image_url,
                   collect({id:o.id,text:coalesce(o.text_vi,''),correct:o.correct}) AS options
            ORDER BY q.grade, q.id
        """, ids=list(ids))
        return [self._question(row) for row in rows]

    def save_attempt(self, user_id: str, result: AttemptResult) -> None:
        """One Neo4j write transaction; no User/Topic/Progress properties are changed."""
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Assessment write requires a Neo4j driver")
        payload = [{"id": f"answer:{result.id.split(':', 1)[1]}:{index}",
                    "question_id": answer.question_id,
                    "selected": list(answer.selected_ids), "correct": answer.correct}
                   for index, answer in enumerate(result.answers)]

        def write(tx):
            count = tx.run("""
                MATCH (u:User {id:$user_id})-[:STUDIES_AT]->(level:Level),
                      (t:Topic {id:$topic_id})
                WHERE level.grade = t.grade AND t.status='published'
                RETURN count(u) AS found
            """, user_id=user_id, topic_id=result.topic_id).single()["found"]
            if count != 1:
                raise ValueError("Người học không ở lớp của chủ đề hoặc chủ đề chưa xuất bản")
            for answer in payload:
                current = tx.run("""
                    MATCH (t:Topic {id:$topic_id})-[:HAS_QUESTION]->(q:Question {id:$question_id})
                    WHERE q.status='published' AND t.status='published'
                    MATCH (q)-[:HAS_OPTION]->(o:Option)
                    RETURN collect(o.id) AS available,
                           collect(CASE WHEN o.correct THEN o.id END) AS correct_ids
                """, topic_id=result.topic_id, question_id=answer["question_id"]).single()
                if (not current or not set(answer["selected"]) <= set(current["available"])
                        or (set(answer["selected"]) == set(current["correct_ids"])) != answer["correct"]):
                    raise ValueError("Câu hỏi hoặc đáp án đã thay đổi")
            tx.run("""
                MATCH (u:User {id:$user_id}), (t:Topic {id:$topic_id})
                CREATE (a:Attempt {id:$id, score:$score, status:'completed',
                                    started_at:datetime($started_at), finished_at:datetime($finished_at),
                                    demo:coalesce(u.demo,false)})
                CREATE (u)-[:ATTEMPTED]->(a)-[:FOR_TOPIC]->(t)
            """, user_id=user_id, topic_id=result.topic_id, id=result.id,
                score=result.score, started_at=result.started_at,
                finished_at=result.finished_at).consume()
            for answer in payload:
                tx.run("""
                    MATCH (a:Attempt {id:$attempt_id}), (q:Question {id:$question_id})
                    CREATE (a)-[:HAS_ANSWER]->(x:AttemptAnswer {
                        id:$id, correct:$correct, demo:coalesce(a.demo,false)})-[:ANSWERS]->(q)
                    WITH x, q
                    UNWIND $selected AS option_id
                    MATCH (q)-[:HAS_OPTION]->(o:Option {id:option_id})
                    CREATE (x)-[:SELECTED]->(o)
                """, attempt_id=result.id, **answer).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def start_test(self, user_id: str, grade: int, topic_id: str, attempt_id: str,
                   question_ids: list[str], option_orders: dict,
                   started_at: str, duration_seconds: int) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Timed test requires a Neo4j driver")

        def write(tx):
            row = tx.run("""
                MATCH (u:User {id:$user_id})-[:STUDIES_AT]->(level:Level {grade:$grade}),
                      (t:Topic {id:$topic_id, grade:$grade})
                WHERE t.status='published'
                MATCH (t)-[:HAS_QUESTION]->(q:Question)
                WHERE q.status='published' AND q.id IN $question_ids
                RETURN count(DISTINCT u) AS user_count,
                       collect(DISTINCT q.id) AS found
            """, user_id=user_id, grade=grade, topic_id=topic_id,
                question_ids=question_ids).single()
            if not row or row["user_count"] != 1 or set(row["found"]) != set(question_ids):
                raise ValueError("Người học hoặc bộ câu hỏi không hợp lệ")
            tx.run("""
                MATCH (u:User {id:$user_id}), (t:Topic {id:$topic_id})
                CREATE (u)-[:ATTEMPTED]->(a:Attempt {
                    id:$attempt_id, status:'draft', mode:'test',
                    started_at:datetime($started_at), duration_seconds:$duration,
                    question_ids:$question_ids, option_orders_json:$option_orders,
                    selections_json:'{}', demo:coalesce(u.demo,false)})-[:FOR_TOPIC]->(t)
            """, user_id=user_id, topic_id=topic_id, attempt_id=attempt_id,
                started_at=started_at, duration=duration_seconds,
                question_ids=question_ids,
                option_orders=json.dumps(option_orders, sort_keys=True)).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def test_draft(self, user_id: str, attempt_id: str) -> dict | None:
        rows = self.db.read("""
            MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt {id:$attempt_id})
                  -[:FOR_TOPIC]->(t:Topic)
            WHERE a.status='draft' AND a.mode='test'
            RETURN a.id AS id, t.id AS topic_id, t.grade AS grade,
                   a.question_ids AS question_ids,
                   a.option_orders_json AS option_orders_json,
                   a.selections_json AS selections_json,
                   toString(a.started_at) AS started_at,
                   a.duration_seconds AS duration_seconds
        """, user_id=user_id, attempt_id=attempt_id)
        if not rows:
            return None
        row = rows[0]
        row["option_orders"] = json.loads(row.pop("option_orders_json"))
        row["selections"] = json.loads(row.pop("selections_json"))
        return row

    def test_drafts(self, user_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt)-[:FOR_TOPIC]->(t:Topic)
            WHERE a.status='draft' AND a.mode='test'
            RETURN a.id AS id, t.id AS topic_id,
                   toString(a.started_at) AS started_at
            ORDER BY a.started_at DESC, a.id
        """, user_id=user_id)

    def save_test_draft(self, user_id: str, attempt_id: str,
                        selections: dict[str, tuple[str, ...]]) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Timed test requires a Neo4j driver")
        serialized = json.dumps({key: list(value) for key, value in selections.items()
                                 if value}, sort_keys=True)

        def write(tx):
            saved = tx.run("""
                MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt {id:$attempt_id})
                SET a.lock=coalesce(a.lock,0)+1
                WITH a
                WHERE a.status='draft' AND a.mode='test'
                  AND datetime() <= a.started_at + duration({seconds:a.duration_seconds})
                SET a.selections_json=$selections
                RETURN a.id AS id
            """, user_id=user_id, attempt_id=attempt_id,
                selections=serialized).single()
            if not saved:
                raise ValueError("Bài kiểm tra đã hết giờ hoặc không thuộc người học")

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def complete_test(self, user_id: str, result: AttemptResult) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Timed test requires a Neo4j driver")
        payload = [{"id": f"answer:{result.id.split(':',1)[1]}:{index}",
                    "question_id": answer.question_id,
                    "selected": list(answer.selected_ids), "correct": answer.correct,
                    "correct_ids": list(answer.correct_ids)}
                   for index, answer in enumerate(result.answers)]
        expected = json.dumps({row["question_id"]: row["selected"] for row in payload
                               if row["selected"]}, sort_keys=True)

        def write(tx):
            draft = tx.run("""
                MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt {id:$attempt_id})
                SET a.lock=coalesce(a.lock,0)+1
                RETURN a.status AS status, a.mode AS mode,
                       a.question_ids AS question_ids,
                       a.selections_json AS selections_json
            """, user_id=user_id, attempt_id=result.id).single()
            if (not draft or draft["status"] != "draft" or draft["mode"] != "test"
                    or draft["question_ids"] != [row["question_id"] for row in payload]
                    or draft["selections_json"] != expected):
                raise ValueError("Bài kiểm tra đã thay đổi hoặc đã nộp")
            for answer in payload:
                current = tx.run("""
                    MATCH (:Attempt {id:$attempt_id})-[:FOR_TOPIC]->(t:Topic)
                          -[:HAS_QUESTION]->(q:Question {id:$question_id})
                    WHERE q.status='published' AND t.status='published'
                    MATCH (q)-[:HAS_OPTION]->(o:Option)
                    RETURN collect(o.id) AS available,
                           collect(CASE WHEN o.correct THEN o.id END) AS correct_ids
                """, attempt_id=result.id, question_id=answer["question_id"]).single()
                if (not current or not set(answer["selected"]) <= set(current["available"])
                        or set(answer["correct_ids"]) != set(current["correct_ids"])
                        or (set(answer["selected"]) == set(current["correct_ids"]))
                        != answer["correct"]):
                    raise ValueError("Nội dung câu hỏi đã thay đổi")
            tx.run("""
                MATCH (:User {id:$user_id})-[:ATTEMPTED]->(a:Attempt {id:$attempt_id})
                SET a.status='completed', a.score=$score,
                    a.finished_at=datetime($finished_at)
            """, user_id=user_id, attempt_id=result.id,
                score=result.score, finished_at=result.finished_at).consume()
            for answer in payload:
                tx.run("""
                    MATCH (a:Attempt {id:$attempt_id}), (q:Question {id:$question_id})
                    CREATE (a)-[:HAS_ANSWER]->(x:AttemptAnswer {
                        id:$id, correct:$correct, demo:coalesce(a.demo,false)})-[:ANSWERS]->(q)
                """, attempt_id=result.id, **answer).consume()
                if answer["selected"]:
                    tx.run("""
                        MATCH (a:AttemptAnswer {id:$id})-[:ANSWERS]->(q:Question)
                        UNWIND $selected AS option_id
                        MATCH (q)-[:HAS_OPTION]->(o:Option {id:option_id})
                        CREATE (a)-[:SELECTED]->(o)
                    """, id=answer["id"], selected=answer["selected"]).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def attempt_detail(self, user_id: str, attempt_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:ATTEMPTED]->(:Attempt {id:$attempt_id})
                  -[:HAS_ANSWER]->(a:AttemptAnswer)-[:ANSWERS]->(q:Question)
            OPTIONAL MATCH (a)-[:SELECTED]->(selected:Option)
            WITH a,q,collect(selected.id) AS selected_ids,
                     collect({id:selected.id,text:selected.text_vi}) AS selected_options
            OPTIONAL MATCH (q)-[:HAS_OPTION]->(correct:Option {correct:true})
            RETURN q.id AS question_id, q.text_vi AS question,
                   a.correct AS correct, selected_ids, selected_options,
                   collect(correct.id) AS correct_ids,
                   collect({id:correct.id,text:correct.text_vi}) AS correct_options,
                   q.explanation_vi AS explanation
            ORDER BY q.id
        """, user_id=user_id, attempt_id=attempt_id)

    def essays(self, grade: int, topic_id: str | None = None) -> list[EssayProblem]:
        rows = self.db.read("""
            MATCH (t:Topic)-[:HAS_ESSAY]->(e:EssayProblem)
            WHERE t.grade=$grade AND t.status='published'
              AND coalesce(e.status,'published')='published'
              AND ($topic_id IS NULL OR t.id=$topic_id)
            OPTIONAL MATCH (e)-[:HAS_HINT]->(h:EssayHint)
            WITH t,e,h ORDER BY h.order
            RETURN e.id AS id, t.id AS topic_id, e.grade AS grade,
                   coalesce(e.prompt_vi,'') AS prompt,
                   coalesce(e.assumptions_vi,'') AS assumptions,
                   coalesce(e.conclusion_vi,'') AS conclusion,
                   coalesce(e.solution_vi,'') AS solution,
                   coalesce(e.image_url,'') AS image_url,
                   coalesce(e.kind,'calculation') AS kind,
                   collect({order:h.order,text:coalesce(h.text_vi,''),
                            image_url:coalesce(h.image_url,'')}) AS hints
            ORDER BY e.id
        """, grade=grade, topic_id=topic_id)
        essays = []
        for row in rows:
            hints = tuple(EssayHint(**hint) for hint in row.pop("hints") if hint["order"] is not None)
            essay = EssayProblem(**row, hints=hints)
            validate_essay(essay)
            essays.append(essay)
        return essays

    def import_batch(self, topic_id: str, grade: int, batch: dict) -> None:
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Assessment import requires a Neo4j driver")

        def write(tx):
            topic = tx.run("""
                MATCH (t:Topic {id:$id, grade:$grade})
                RETURN count(t) AS found
            """, id=topic_id, grade=grade).single()
            if not topic or topic["found"] != 1:
                raise ValueError("Chủ đề không tồn tại hoặc sai lớp")
            tx.run("""
                MATCH (t:Topic {id:$topic_id})
                UNWIND $questions AS item
                CREATE (t)-[:HAS_QUESTION]->(q:Question {
                    id:item.id, grade:item.grade, type:item.type,
                    difficulty:item.difficulty, status:item.status,
                    text_vi:item.text_vi, explanation_vi:item.explanation_vi,
                    image_url:item.image_url, demo:coalesce(t.demo,false)})
                WITH q,item
                UNWIND item.options AS option
                CREATE (q)-[:HAS_OPTION]->(:Option {
                    id:option.id, text_vi:option.text_vi, correct:option.correct,
                    demo:coalesce(q.demo,false)})
            """, topic_id=topic_id, questions=batch["questions"]).consume()
            tx.run("""
                MATCH (t:Topic {id:$topic_id})
                UNWIND $essays AS item
                CREATE (t)-[:HAS_ESSAY]->(e:EssayProblem {
                    id:item.id, grade:item.grade, kind:item.kind, status:item.status,
                    prompt_vi:item.prompt_vi, assumptions_vi:item.assumptions_vi,
                    conclusion_vi:item.conclusion_vi, solution_vi:item.solution_vi,
                    image_url:item.image_url, demo:coalesce(t.demo,false)})
                FOREACH (hint IN item.hints |
                    CREATE (e)-[:HAS_HINT]->(:EssayHint {
                        id:hint.id, order:hint.order, text_vi:hint.text_vi,
                        image_url:hint.image_url, demo:coalesce(e.demo,false)}))
            """, topic_id=topic_id, essays=batch["essays"]).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def preview_assessment(self, topic_id: str) -> dict[str, list[dict]]:
        questions = self.db.read("""
            MATCH (:Topic {id:$topic_id})-[:HAS_QUESTION]->(q:Question)
            OPTIONAL MATCH (q)-[:HAS_OPTION]->(o:Option)
            WITH q,o ORDER BY o.id
            RETURN q.id AS id, q.status AS status, q.grade AS grade,
                   q.type AS type, q.difficulty AS difficulty,
                   q.text_vi AS text_vi, q.explanation_vi AS explanation_vi,
                   coalesce(q.image_url,'') AS image_url,
                   collect({id:o.id,text_vi:o.text_vi,correct:o.correct}) AS options
            ORDER BY q.id
        """, topic_id=topic_id)
        essays = self.db.read("""
            MATCH (:Topic {id:$topic_id})-[:HAS_ESSAY]->(e:EssayProblem)
            OPTIONAL MATCH (e)-[:HAS_HINT]->(h:EssayHint)
            WITH e,h ORDER BY h.order
            RETURN e.id AS id, coalesce(e.status,'published') AS status,
                   e.grade AS grade, e.kind AS kind, e.prompt_vi AS prompt_vi,
                   e.assumptions_vi AS assumptions_vi,
                   e.conclusion_vi AS conclusion_vi,
                   e.solution_vi AS solution_vi,
                   coalesce(e.image_url,'') AS image_url,
                   collect({id:h.id,order:h.order,text_vi:h.text_vi,
                            image_url:h.image_url}) AS hints
            ORDER BY e.id
        """, topic_id=topic_id)
        for question in questions:
            question["options"] = [item for item in question["options"] if item["id"]]
        for essay in essays:
            essay["hints"] = [item for item in essay["hints"] if item["id"]]
        return {"questions": questions, "essays": essays}

    def save_essay_review(self, user_id: str, essay_id: str, review_id: str,
                          rating: str, hints_used: int, created_at: str,
                          answer_text: str = "") -> None:
        self._ensure_review_schema()
        driver = getattr(self.db, "driver", None)
        if driver is None:
            raise RuntimeError("Essay review requires a Neo4j driver")

        def write(tx):
            row = tx.run("""
                MATCH (u:User {id:$user_id})-[:STUDIES_AT]->(level:Level),
                      (t:Topic)-[:HAS_ESSAY]->(e:EssayProblem {id:$essay_id})
                WHERE level.grade=t.grade AND t.status='published'
                  AND coalesce(e.status,'published')='published'
                OPTIONAL MATCH (e)-[:HAS_HINT]->(h:EssayHint)
                RETURN count(DISTINCT u) AS found, count(DISTINCT h) AS hint_count
            """, user_id=user_id, essay_id=essay_id).single()
            if not row or row["found"] != 1 or hints_used > row["hint_count"]:
                raise ValueError("Đề không phù hợp với người học hoặc số gợi ý không hợp lệ")
            tx.run("""
                MATCH (u:User {id:$user_id}), (e:EssayProblem {id:$essay_id})
                CREATE (u)-[:REVIEWED_ESSAY]->(r:EssayReview {
                    id:$review_id, rating:$rating, hints_used:$hints_used,
                    answer_text:$answer_text,
                    created_at:datetime($created_at), demo:coalesce(u.demo,false)})-[:FOR_ESSAY]->(e)
            """, user_id=user_id, essay_id=essay_id, review_id=review_id,
                rating=rating, hints_used=hints_used, created_at=created_at,
                answer_text=answer_text).consume()

        with driver.session(database=self.db.database) as session:
            session.execute_write(write)

    def essay_reviews(self, user_id: str) -> list[dict]:
        return self.db.read("""
            MATCH (:User {id:$user_id})-[:REVIEWED_ESSAY]->(r:EssayReview)
                  -[:FOR_ESSAY]->(e:EssayProblem)
            RETURN r.id AS id, e.id AS essay_id, r.rating AS rating,
                   r.hints_used AS hints_used, coalesce(r.answer_text,'') AS answer_text,
                   toString(r.created_at) AS created_at
            ORDER BY r.created_at DESC, r.id
        """, user_id=user_id)
