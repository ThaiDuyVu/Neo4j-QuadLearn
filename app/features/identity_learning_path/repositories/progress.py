# DOMAIN OWNER: VU. Chỉ ghi Progress và các cạnh học tập của User.
from ..models.errors import IdentityError


class ProgressRepository:
    def __init__(self, db):
        self.db = db

    def snapshot(self, user_id):
        completed = self.db.read(
            "MATCH (:User {id:$id})-[:COMPLETED]->(l:Lesson) RETURN l.id AS id",
            id=user_id,
        )
        opened = self.db.read(
            "MATCH (:User {id:$id})-[:HAS_PROGRESS]->(p:Progress)-[:FOR_LEVEL]->(l:Level) WHERE p.unlocked=true RETURN l.grade AS grade",
            id=user_id,
        )
        return {x["id"] for x in completed}, {x["grade"] for x in opened}

    def projections(self, user_id, rows):
        self.db.write(
            """
            MATCH (u:User {id:$id}) WHERE u.status='active' AND coalesce(u.demo,false)=false
            UNWIND $rows AS row MATCH (l:Level {grade:row.grade})
            MERGE (p:Progress {user_id:u.id,level_id:l.id})
            ON CREATE SET p.id=row.id, p.unlocked=false
            SET p.completion=row.completion,p.average_score=row.average_score,p.updated_at=datetime()
            MERGE (u)-[:HAS_PROGRESS]->(p) MERGE (p)-[:FOR_LEVEL]->(l)
        """,
            id=user_id,
            rows=rows,
        )

    def mark_lesson(self, user_id, lesson_id, complete, projection_rows=None):
        # Khóa user trước, kiểm active/verified/consent và published ngay trong transaction.
        def work(tx):
            row = tx.run(
                """
                MATCH (u:User {id:$id}) SET u.progress_lock=coalesce(u.progress_lock,0)+1
                WITH u WHERE u.status='active' AND u.email_verified=true AND coalesce(u.demo,false)=false
                   AND (u.guardian_required=false OR u.guardian_consent=true)
                MATCH (l:Lesson {id:$lesson,status:'published'}) RETURN u.id AS id
            """,
                id=user_id,
                lesson=lesson_id,
            ).single()
            if not row:
                raise IdentityError("Không được ghi tiến độ cho tài khoản/bài học này.")
            if complete:
                tx.run(
                    """
                    MATCH (u:User {id:$id}),(l:Lesson {id:$lesson})
                    MERGE (u)-[c:COMPLETED]->(l) ON CREATE SET c.completed_at=datetime()
                    MERGE (u)-[r:LEARNING]->(l) SET r.status='completed',r.last_seen=datetime()
                """,
                    id=user_id,
                    lesson=lesson_id,
                ).consume()
            else:
                tx.run(
                    """
                    MATCH (u:User {id:$id}),(l:Lesson {id:$lesson})
                    WHERE NOT EXISTS { MATCH (u)-[:COMPLETED]->(l) }
                    MERGE (u)-[r:LEARNING]->(l) SET r.status='in_progress',r.last_seen=datetime()
                """,
                    id=user_id,
                    lesson=lesson_id,
                ).consume()
            if complete and projection_rows is not None:
                # Cạnh COMPLETED và projection ghi cùng transaction. Điểm lấy qua contract Đạt,
                # số bài/hoàn thành tính lại trong transaction từ published graph hiện tại.
                tx.run(
                    """
                    MATCH (u:User {id:$id}) UNWIND $rows AS row MATCH (l:Level {grade:row.grade})
                    OPTIONAL MATCH (l)-[:HAS_CHAPTER]->(chapter:Chapter)-[:HAS_TOPIC]->(topic:Topic)-[:HAS_LESSON]->(lesson:Lesson)
                    WHERE lesson.status='published' AND topic.status='published'
                      AND coalesce(chapter.status,'published')='published'
                      AND lesson.grade=row.grade AND topic.grade=row.grade
                    WITH u,l,row,collect(DISTINCT lesson) AS lessons
                    WITH u,l,row,size(lessons) AS total,
                      size([lesson IN lessons WHERE EXISTS { MATCH (u)-[:COMPLETED]->(lesson) }]) AS done
                    MERGE (p:Progress {user_id:u.id,level_id:l.id})
                    ON CREATE SET p.id=row.id,p.unlocked=false
                    SET p.completion=CASE WHEN total=0 THEN 0.0 ELSE 100.0*done/total END,
                        p.average_score=row.average_score,p.updated_at=datetime()
                    MERGE (u)-[:HAS_PROGRESS]->(p) MERGE (p)-[:FOR_LEVEL]->(l)
                """,
                    id=user_id,
                    rows=projection_rows,
                ).consume()

        self.db.transaction(work)

    def resume_id(self, user_id):
        rows = self.db.read(
            """
            MATCH (:User {id:$id})-[r:LEARNING {status:'in_progress'}]->(l:Lesson)
            WHERE l.status='published' RETURN l.id AS id ORDER BY r.last_seen DESC,l.id LIMIT 1
        """,
            id=user_id,
        )
        return rows[0]["id"] if rows else None

    def change_level(self, user_id, grade, reason):
        def work(tx):
            row = tx.run(
                """
                MATCH (u:User {id:$id}) SET u.progress_lock=coalesce(u.progress_lock,0)+1
                WITH u WHERE u.status='active' MATCH (l:Level {grade:$grade})
                RETURN l.id AS level
            """,
                id=user_id,
                grade=grade,
            ).single()
            if not row:
                raise IdentityError(
                    "Không tìm thấy cấp độ hoặc tài khoản không hoạt động."
                )
            tx.run(
                "MATCH (:User {id:$id})-[old:STUDIES_AT]->() DELETE old", id=user_id
            ).consume()
            tx.run(
                """
                MATCH (u:User {id:$id}),(l:Level {id:$level}) MERGE (u)-[:STUDIES_AT]->(l)
                MERGE (p:Progress {user_id:u.id,level_id:l.id})
                ON CREATE SET p.id=$progress
                SET p.unlocked=true,p.unlock_reason=$reason,p.unlocked_at=coalesce(p.unlocked_at,datetime())
                MERGE (u)-[:HAS_PROGRESS]->(p) MERGE (p)-[:FOR_LEVEL]->(l)
            """,
                id=user_id,
                level=row["level"],
                progress=f"progress:{user_id}:{grade}",
                reason=reason,
            ).consume()

        self.db.transaction(work)
