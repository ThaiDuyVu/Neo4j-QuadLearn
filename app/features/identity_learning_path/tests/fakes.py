from datetime import datetime, timezone
from copy import deepcopy
from app.shared.models.dto import (
    CurrentUser,
    LessonSummary,
    AttemptSummary,
    CatalogLesson,
)
from app.features.identity_learning_path.models.errors import IdentityError
from app.features.identity_learning_path.services.security import digest


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 8, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


class MemoryIdentityRepository:
    def __init__(self):
        self.users_by_id = {}
        self.tokens = {}
        self.sessions = {}

    def create(self, fields, tokens):
        if any(u["email"] == fields["email"] for u in self.users_by_id.values()):
            raise IdentityError("Email đã được sử dụng.")
        self.users_by_id[fields["id"]] = deepcopy(fields)
        for t in tokens:
            self.tokens[t["hash"]] = deepcopy(t) | {"user_id": fields["id"]}

    def mutate(self, identifier, callback, by_email=False):
        record = (
            next(
                (u for u in self.users_by_id.values() if u["email"] == identifier), None
            )
            if by_email
            else self.users_by_id.get(identifier)
        )
        updates, result = callback(deepcopy(record))
        if record:
            record.update(updates)
        return result

    def profile(self, uid):
        u = self.users_by_id.get(uid)
        return dict(u, grade=u.get("grade", u["starting_grade"])) if u else None

    def user_by_id(self, uid):
        u = self.profile(uid)
        return (
            CurrentUser(uid, u["name"], u["grade"], u["role"], u.get("demo", False))
            if u
            else None
        )

    def consume_token(self, token_hash, kind, now, password_hash=None):
        t = self.tokens.get(token_hash)
        if not t or t["kind"] != kind or t.get("used_at") or t["expires_at"] <= now:
            raise IdentityError("Token không hợp lệ.")
        u = self.users_by_id[t["user_id"]]
        if u["status"] not in ("pending", "active"):
            raise IdentityError("Token không hợp lệ.")
        if kind == "verify":
            u["email_verified"] = True
        elif kind == "guardian":
            u["guardian_consent"] = True
        else:
            u.update(
                password_hash=password_hash,
                auth_version=u["auth_version"] + 1,
                failed_logins=0,
                locked_until=None,
            )
            for other in self.tokens.values():
                if other["kind"] == "reset" and other["user_id"] == u["id"]:
                    other["used_at"] = now
        if u["email_verified"] and (
            not u["guardian_required"] or u["guardian_consent"]
        ):
            u["status"] = "active"
        t["used_at"] = now
        return u["id"]

    def create_session(self, uid, version, token_hash, now):
        u = self.users_by_id[uid]
        if u["status"] != "active" or u["auth_version"] != version:
            raise IdentityError("User changed")
        self.sessions[token_hash] = dict(user_id=uid, version=version, last_seen=now)

    def resolve_session(self, token_hash, now, cutoff, app_env):
        s = self.sessions.get(token_hash)
        if not s:
            return None
        u = self.users_by_id[s["user_id"]]
        if (
            u["status"] != "active"
            or u["auth_version"] != s["version"]
            or s["last_seen"] <= cutoff
            or app_env != "development"
        ):
            return None
        s["last_seen"] = now
        return self.user_by_id(u["id"])

    def delete_session(self, token_hash):
        self.sessions.pop(token_hash, None)

    def reset_token(self, email, token):
        u = next(
            (
                u
                for u in self.users_by_id.values()
                if u["email"] == email and u["status"] in ("active", "pending")
            ),
            None,
        )
        if not u:
            return False
        self.tokens[token["hash"]] = deepcopy(token) | {"user_id": u["id"]}
        return True

    def users(self, term):
        return []


class MemoryProgressRepository:
    def __init__(self):
        self.completed = set()
        self.opened = {}
        self.resume = None
        self.writes = 0

    def snapshot(self, uid):
        return set(self.completed), self.opened.get(uid, set())

    def projections(self, uid, rows):
        self.rows = rows

    def mark_lesson(self, uid, lesson_id, complete, projection_rows=None):
        self.writes += 1
        if complete:
            self.completed.add(lesson_id)
        else:
            self.resume = lesson_id
        if projection_rows is not None:
            self.rows = [
                dict(
                    row,
                    completion=100
                    * len(self.completed.intersection(row["lesson_ids"]))
                    / len(row["lesson_ids"])
                    if row["lesson_ids"]
                    else 0,
                )
                for row in projection_rows
            ]

    def resume_id(self, uid):
        return self.resume

    def change_level(self, uid, grade, reason):
        self.opened.setdefault(uid, set()).add(grade)
        self.changed = (uid, grade, reason)


class Content:
    def __init__(self):
        self.items = {
            6: [
                LessonSummary("lesson:6:a", "A", 6, "topic:6:a"),
                LessonSummary("lesson:6:b", "B", 6, "topic:6:b"),
            ],
            7: [LessonSummary("lesson:7:a", "C", 7, "topic:7:a")],
            8: [],
            9: [],
        }

    def lessons(self, grade):
        return self.items[grade]

    def prerequisites(self, id):
        return self.items[6]

    def catalog(self, grade):
        return [
            CatalogLesson(l, "chapter:test", "Chapter", l.topic_id, "understand")
            for l in self.lessons(grade)
        ]

    def ai_context(self, id):
        return []


class Assessment:
    def __init__(self):
        self.items = []

    def attempts(self, uid):
        return self.items
