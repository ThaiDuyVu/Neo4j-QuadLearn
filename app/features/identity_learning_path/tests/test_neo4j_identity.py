"""Integration có opt-in; chỉ tạo/xóa dữ liệu user:test UUID do test sở hữu."""

import os
from datetime import timedelta
from uuid import uuid4
import pytest
from app.core.config import Settings
from app.core.database import Database
from app.core.bootstrap import build_context
from app.features.identity_learning_path.repositories.identity import IdentityRepository
from app.features.identity_learning_path.services.auth import AuthService
from app.features.identity_learning_path.services.identity import IdentityService
from app.features.identity_learning_path.services.learning_path import (
    LearningPathService,
)
from app.features.identity_learning_path.repositories.progress import ProgressRepository
from app.features.identity_learning_path.models.errors import IdentityError
from app.features.identity_learning_path.models.policy import IdentityPolicy
from app.core.catalog import GraphLearningCatalog
from app.shared.models.dto import AttemptSummary
from .fakes import Clock

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("QUADLEARN_INTEGRATION") != "1",
        reason="Explicit local Neo4j opt-in required",
    ),
]


@pytest.fixture
def env():
    settings = Settings.load()
    assert settings.app_env == "development"
    db = Database(settings)
    db.verify()
    repo = IdentityRepository(db)
    clock = Clock()
    auth = AuthService(repo, clock=clock)
    identity = IdentityService(repo, {}, clock=clock)
    email = f"test-{uuid4()}@example.invalid"
    uid, tokens = auth.register(
        "Test integration", email, "TestPass123", 6, 13, "guardian@example.invalid"
    )
    try:
        yield db, repo, clock, auth, identity, email, uid, tokens
    finally:
        # Chỉ xóa identity-owned nodes tạo bởi fixture; không sửa dữ liệu Sơn/Đạt.
        db.write(
            "MATCH (u:User {id:$id}) OPTIONAL MATCH (u)-[:HAS_AUTH_TOKEN|HAS_AUTH_SESSION|HAS_PROGRESS]->(n) WITH u,collect(n) AS nodes FOREACH (n IN nodes | DETACH DELETE n) DETACH DELETE u",
            id=uid,
        )
        db.close()


def activate(env):
    db, repo, clock, auth, identity, email, uid, tokens = env
    auth.activate(tokens["verify"], "verify")
    auth.activate(tokens["guardian"], "guardian")
    identity.login(auth.login(email, "TestPass123"))


def test_neo4j_registration_guardian_unique_and_session(env):
    db, repo, clock, auth, identity, email, uid, tokens = env
    with pytest.raises(IdentityError):
        auth.login(email, "TestPass123")
    auth.activate(tokens["verify"], "verify")
    with pytest.raises(IdentityError):
        auth.login(email, "TestPass123")
    auth.activate(tokens["guardian"], "guardian")
    with pytest.raises(IdentityError):
        auth.activate(tokens["guardian"], "guardian")
    identity.login(auth.login(email, "TestPass123"))
    assert identity.current_user().id == uid and identity.current_user().demo is False
    with pytest.raises(IdentityError):
        auth.register("Duplicate", email.upper(), "TestPass123", 6, 18)
    assert (
        db.read(
            "MATCH (u:User {id:$id})-[:STUDIES_AT]->(l) RETURN count(l) AS n", id=uid
        )[0]["n"]
        == 1
    )


def test_neo4j_login_lockout_reset_reuse_expiry_and_revocation(env):
    activate(env)
    db, repo, clock, auth, identity, email, uid, tokens = env
    for _ in range(5):
        with pytest.raises(IdentityError):
            auth.login(email, "wrong")
    with pytest.raises(IdentityError):
        auth.login(email, "TestPass123")
    clock.now += timedelta(minutes=16)
    assert auth.login(email, "TestPass123")
    raw = auth.request_reset(email)
    auth.reset_password(raw, "NewPass456")
    assert identity.current_user() is None
    with pytest.raises(IdentityError):
        auth.reset_password(raw, "AgainPass789")
    identity.login(auth.login(email, "NewPass456"))
    raw = auth.request_reset(email)
    clock.now += timedelta(minutes=30)
    with pytest.raises(IdentityError):
        auth.reset_password(raw, "AgainPass789")
    clock.now += timedelta(days=7)
    assert identity.current_user() is None


def test_neo4j_progress_published_idempotent_unlock_and_admin_guard(env):
    activate(env)
    db, repo, clock, auth, identity, email, uid, tokens = env
    base = build_context(db)

    class Assessment:
        def attempts(self, id):
            return [
                AttemptSummary("fixture:read-only", "topic:6:rectangle", 6, "completed")
            ]

    path = LearningPathService(
        ProgressRepository(db),
        identity,
        base.content,
        Assessment(),
        GraphLearningCatalog(db),
    )
    path.start_lesson(uid, "lesson:6:rectangle")
    assert path.resume_lesson(uid).id == "lesson:6:rectangle"
    with pytest.raises(IdentityError):
        path.complete_lesson(uid, "lesson:9:cyclic")
    path.complete_lesson(uid, "lesson:6:rectangle")
    path.complete_lesson(uid, "lesson:6:rectangle")
    # Ghi cùng bài hai lần vẫn chỉ có một quan hệ COMPLETED.
    assert db.read(
        "MATCH (:User {id:$id})-[:COMPLETED]->() RETURN count(*) AS n", id=uid
    )[0]["n"] == 1
    lessons = base.content.lessons(6)
    for lesson in lessons:
        path.complete_lesson(uid, lesson.id)
    assert path.levels(uid)[0].completion == 100
    assert path.resume_lesson(uid) is None
    assert path.access(uid, 7)
    path.change_level(7)
    assert identity.current_user().grade == 7
    assert (
        db.read(
            "MATCH (:User {id:$id})-[r:COMPLETED]->() RETURN count(r) AS n", id=uid
        )[0]["n"]
        == len(lessons)
    )
    assert (
        db.read(
            "MATCH (:User {id:$id})-[:STUDIES_AT]->() RETURN count(*) AS n", id=uid
        )[0]["n"]
        == 1
    )
    with pytest.raises(IdentityError):
        identity.search_users("")
    with pytest.raises(IdentityError):
        path.complete_lesson("user:demo-student", "lesson:6:rectangle")
    assert path.breakdown(uid, 6)[0]["completion"] == 100


def test_neo4j_profile_change_password_and_blocked_sessions(env):
    activate(env)
    db, repo, clock, auth, identity, email, uid, tokens = env
    identity.update_profile("Tên cập nhật", "en")
    assert identity.profile()["language"] == "en"
    auth.change_password(identity, "TestPass123", "NewPass456")
    assert identity.current_user() is None
    identity.login(auth.login(email, "NewPass456"))
    repo.mutate(
        uid,
        lambda user: (
            {"status": "blocked", "auth_version": user["auth_version"] + 1},
            None,
        ),
    )
    assert identity.current_user() is None
    with pytest.raises(IdentityError):
        auth.login(email, "NewPass456")
