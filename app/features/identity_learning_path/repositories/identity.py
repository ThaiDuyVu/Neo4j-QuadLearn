# DOMAIN OWNER: VU. CORE CONNECT: mọi Cypher AUTH/User ở đây, không ở page.
from uuid import uuid4
from neo4j.exceptions import ConstraintError
from app.shared.models.dto import CurrentUser
from ..models.errors import IdentityError


class IdentityRepository:
    def __init__(self, db):
        self.db = db

    def user_by_id(self, user_id):
        rows = self.db.read(
            """
            MATCH (u:User {id:$id})-[:STUDIES_AT]->(l:Level)
            RETURN u.id AS id, u.name AS name, l.grade AS grade, u.role AS role,
                   coalesce(u.demo,false) AS demo
        """,
            id=user_id,
        )
        return CurrentUser(**rows[0]) if rows else None

    def profile(self, user_id):
        rows = self.db.read(
            """
            MATCH (u:User {id:$id})-[:STUDIES_AT]->(l:Level)
            RETURN properties(u) AS user, l.grade AS grade
        """,
            id=user_id,
        )
        if not rows:
            return None
        return dict(rows[0]["user"], grade=rows[0]["grade"])

    def create(self, fields, tokens):
        def work(tx):
            level = tx.run(
                "MATCH (l:Level {grade:$grade}) RETURN l.id AS id",
                grade=fields["starting_grade"],
            ).single()
            if not level:
                raise IdentityError("Chưa có cấp độ. Chạy seed trước khi đăng ký.")
            tx.run(
                """
                MATCH (l:Level {id:$level}) CREATE (u:User) SET u=$fields
                CREATE (u)-[:STUDIES_AT]->(l)
                MERGE (p:Progress {id:$progress})
                SET p.user_id=u.id, p.level_id=l.id, p.unlocked=true
                MERGE (u)-[:HAS_PROGRESS]->(p) MERGE (p)-[:FOR_LEVEL]->(l)
            """,
                level=level["id"],
                fields=fields,
                progress=f"progress:{fields['id']}:{fields['starting_grade']}",
            ).consume()
            for token in tokens:
                tx.run(
                    "MATCH (u:User {id:$id}) CREATE (t:AuthToken) SET t=$token CREATE (u)-[:HAS_AUTH_TOKEN]->(t)",
                    id=fields["id"],
                    token=token,
                ).consume()

        try:
            self.db.transaction(work)
        except ConstraintError as error:
            raise IdentityError("Email đã được sử dụng.") from error

    def mutate(self, identifier, callback, by_email=False):
        """Khóa User trong write transaction trước đọc: tránh lost update login/đổi password."""
        key = (
            "email" if by_email else "id"
        )  # allowlist nội bộ, không nhận tên field từ UI.

        def work(tx):
            row = tx.run(
                f"MATCH (u:User {{{key}:$id}}) SET u.auth_lock=coalesce(u.auth_lock,0)+1 RETURN properties(u) AS user",
                id=identifier,
            ).single()
            if not row:
                return callback(None)[1]
            updates, result = callback(dict(row["user"]))
            if updates:
                tx.run(
                    "MATCH (u:User {id:$id}) SET u += $updates",
                    id=row["user"]["id"],
                    updates=updates,
                ).consume()
            return result

        return self.db.transaction(work)

    def consume_token(self, token_hash, kind, now, password_hash=None):
        def work(tx):
            row = tx.run(
                """
                MATCH (u:User)-[:HAS_AUTH_TOKEN]->(t:AuthToken {hash:$hash,kind:$kind})
                SET u.auth_lock=coalesce(u.auth_lock,0)+1
                WITH u,t WHERE t.used_at IS NULL AND t.expires_at > $now
                  AND u.status IN ['pending','active']
                RETURN u.id AS id, properties(u) AS user, t.id AS token_id
            """,
                hash=token_hash,
                kind=kind,
                now=now,
            ).single()
            if not row:
                raise IdentityError("Token không hợp lệ, đã dùng hoặc đã hết hạn.")
            user = row["user"]
            updates = (
                {"email_verified": True}
                if kind == "verify"
                else {"guardian_consent": True}
                if kind == "guardian"
                else {
                    "password_hash": password_hash,
                    "auth_version": user.get("auth_version", 0) + 1,
                    "failed_logins": 0,
                    "locked_until": None,
                }
            )
            if kind != "reset":
                verified = updates.get(
                    "email_verified", user.get("email_verified", False)
                )
                consent = updates.get(
                    "guardian_consent", user.get("guardian_consent", False)
                )
                if verified and (not user.get("guardian_required") or consent):
                    updates["status"] = "active"
            tx.run(
                "MATCH (u:User {id:$id}) SET u += $updates",
                id=row["id"],
                updates=updates,
            ).consume()
            if kind == "reset":
                tx.run(
                    "MATCH (:User {id:$id})-[:HAS_AUTH_TOKEN]->(t:AuthToken {kind:'reset'}) WHERE t.used_at IS NULL SET t.used_at=$now",
                    id=row["id"],
                    now=now,
                ).consume()
            else:
                tx.run(
                    "MATCH (t:AuthToken {id:$id}) SET t.used_at=$now",
                    id=row["token_id"],
                    now=now,
                ).consume()
            return row["id"]

        return self.db.transaction(work)

    def reset_token(self, email, token):
        # Không gửi email, không trả thông tin tồn tại tài khoản ngoài chế độ dev.
        rows = self.db.write(
            """
            MATCH (u:User {email:$email}) WHERE u.status IN ['active','pending'] AND coalesce(u.demo,false)=false
            CREATE (t:AuthToken) SET t=$token CREATE (u)-[:HAS_AUTH_TOKEN]->(t) RETURN t.id AS id
        """,
            email=email,
            token=token,
        )
        return bool(rows)

    def create_session(self, user_id, version, token_hash, now):
        rows = self.db.write(
            """
            MATCH (u:User {id:$id}) SET u.auth_lock=coalesce(u.auth_lock,0)+1
            WITH u WHERE u.status='active' AND u.auth_version=$version
            CREATE (s:AuthSession {id:$session, hash:$hash, last_seen:$now, auth_version:$version})
            CREATE (u)-[:HAS_AUTH_SESSION]->(s) RETURN s.id AS id
        """,
            id=user_id,
            version=version,
            session=f"session:{uuid4()}",
            hash=token_hash,
            now=now,
        )
        if not rows:
            raise IdentityError("Tài khoản thay đổi; vui lòng đăng nhập lại.")

    def resolve_session(self, token_hash, now, cutoff, app_env):
        rows = self.db.write(
            """
            MATCH (u:User)-[:HAS_AUTH_SESSION]->(s:AuthSession {hash:$hash})
            SET u.auth_lock=coalesce(u.auth_lock,0)+1
            WITH u,s WHERE u.status='active' AND s.auth_version=u.auth_version AND s.last_seen > $cutoff
              AND (u.activation_channel <> 'development' OR $env='development')
            MATCH (u)-[:STUDIES_AT]->(l:Level)
            SET s.last_seen=$now
            RETURN u.id AS id, u.name AS name, u.role AS role, l.grade AS grade, false AS demo
        """,
            hash=token_hash,
            now=now,
            cutoff=cutoff,
            env=app_env,
        )
        return CurrentUser(**rows[0]) if rows else None

    def delete_session(self, token_hash):
        self.db.write(
            "MATCH (s:AuthSession {hash:$hash}) DETACH DELETE s", hash=token_hash
        )

    def users(self, term):
        return self.db.read(
            """
            MATCH (u:User)-[:STUDIES_AT]->(l:Level)
            WHERE toLower(u.name) CONTAINS $term OR toLower(u.email) CONTAINS $term
            RETURN u.id AS id, u.name AS name, u.email AS email, u.role AS role,
                   u.status AS status, l.grade AS grade ORDER BY u.name LIMIT 100
        """,
            term=term.lower().strip(),
        )
