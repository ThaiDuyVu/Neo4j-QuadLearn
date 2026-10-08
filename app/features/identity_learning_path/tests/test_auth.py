from datetime import timedelta
import pytest
from app.features.identity_learning_path.services.auth import AuthService
from app.features.identity_learning_path.services.identity import IdentityService
from app.features.identity_learning_path.services.security import (
    validate_password,
    normalize_email,
    verify_password,
    digest,
)
from app.features.identity_learning_path.models.errors import IdentityError
from app.features.identity_learning_path.models.policy import IdentityPolicy
from .fakes import Clock, MemoryIdentityRepository


@pytest.fixture
def env():
    repo = MemoryIdentityRepository()
    clock = Clock()
    auth = AuthService(repo, clock=clock)
    identity = IdentityService(repo, {}, clock=clock)
    return repo, clock, auth, identity


def active(env, age=18):
    repo, clock, auth, identity = env
    uid, tokens = auth.register(
        "Học sinh",
        " TEST@example.invalid ",
        "TestPass123",
        6,
        age,
        "guardian@example.invalid",
    )
    auth.activate(tokens["verify"], "verify")
    if age < 16:
        auth.activate(tokens["guardian"], "guardian")
    identity.login(auth.login("test@example.invalid", "TestPass123"))
    return uid


@pytest.mark.parametrize("password", ["short1", "abcdefgh", "12345678", "a" * 257])
def test_invalid_password(password):
    with pytest.raises(IdentityError):
        validate_password(password)


@pytest.mark.parametrize("email", ["bad", "a@@b.com", "x y@z.com"])
def test_invalid_email(email):
    with pytest.raises(IdentityError):
        normalize_email(email)


def test_register_normalizes_and_hashes_no_plaintext(env):
    uid = active(env)
    record = env[0].users_by_id[uid]
    assert record["email"] == "test@example.invalid"
    assert record["password_hash"].startswith("$argon2id$")
    assert "TestPass123" not in repr(record)
    assert verify_password(record["password_hash"], "TestPass123")
    assert not verify_password(record["password_hash"], "wrong")
    with pytest.raises(IdentityError):
        env[2].register("Other", "TEST@EXAMPLE.INVALID", "Other123", 6, 18)


def test_guardian_activation_is_required(env):
    repo, clock, auth, identity = env
    uid, tokens = auth.register(
        "Student",
        "child@example.invalid",
        "TestPass123",
        6,
        13,
        "guardian@example.invalid",
    )
    auth.activate(tokens["verify"], "verify")
    assert repo.users_by_id[uid]["status"] == "pending"
    with pytest.raises(IdentityError):
        auth.login("child@example.invalid", "TestPass123")
    auth.activate(tokens["guardian"], "guardian")
    assert repo.users_by_id[uid]["status"] == "active"
    with pytest.raises(IdentityError):
        auth.activate(tokens["guardian"], "guardian")


def test_guardian_email_cannot_be_self(env):
    with pytest.raises(IdentityError):
        env[2].register(
            "Student",
            "child@example.invalid",
            "TestPass123",
            6,
            13,
            "CHILD@example.invalid",
        )


def test_five_failures_lock_then_timeout_recovers(env):
    uid = active(env)
    repo, clock, auth, identity = env
    for _ in range(5):
        with pytest.raises(IdentityError):
            auth.login("test@example.invalid", "bad")
    assert repo.users_by_id[uid]["failed_logins"] == 5
    with pytest.raises(IdentityError):
        auth.login("test@example.invalid", "TestPass123")
    clock.now += timedelta(minutes=15)
    identity.login(auth.login("test@example.invalid", "TestPass123"))
    assert identity.current_user().id == uid
    assert repo.users_by_id[uid]["failed_logins"] == 0


def test_failed_login_after_lock_timeout_starts_new_count(env):
    uid = active(env)
    repo, clock, auth, _ = env
    for _ in range(5):
        with pytest.raises(IdentityError):
            auth.login("test@example.invalid", "bad")
    clock.now += timedelta(minutes=16)
    with pytest.raises(IdentityError):
        auth.login("test@example.invalid", "bad")
    assert repo.users_by_id[uid]["failed_logins"] == 1


def test_session_inactivity_expiry_and_logout(env):
    active(env)
    repo, clock, auth, identity = env
    clock.now += timedelta(days=6)
    assert identity.current_user()
    clock.now += timedelta(days=7)
    assert identity.current_user() is None
    identity.login(auth.login("test@example.invalid", "TestPass123"))
    identity.logout()
    assert identity.current_user() is None


def test_reset_single_use_invalidates_all_sessions(env):
    active(env)
    repo, clock, auth, identity = env
    raw = auth.request_reset("test@example.invalid")
    assert raw not in repr(repo.tokens)
    auth.reset_password(raw, "NewPass456")
    assert identity.current_user() is None
    with pytest.raises(IdentityError):
        auth.reset_password(raw, "AgainPass789")
    with pytest.raises(IdentityError):
        auth.login("test@example.invalid", "TestPass123")
    assert auth.login("test@example.invalid", "NewPass456")


def test_reset_expiry_30_minutes(env):
    active(env)
    raw = env[2].request_reset("test@example.invalid")
    env[1].now += timedelta(minutes=30)
    with pytest.raises(IdentityError):
        env[2].reset_password(raw, "NewPass456")


def test_change_password_requires_old_and_revokes_session(env):
    active(env)
    repo, clock, auth, identity = env
    with pytest.raises(IdentityError):
        auth.change_password(identity, "wrong", "NewPass456")
    auth.change_password(identity, "TestPass123", "NewPass456")
    assert identity.current_user() is None


def test_guest_impersonation_and_student_admin_denied(env):
    with pytest.raises(IdentityError):
        env[3].require_user()
    active(env)
    with pytest.raises(IdentityError):
        env[3].require_user("user:other")
    with pytest.raises(IdentityError):
        env[3].require_user(admin=True)


def test_profile_does_not_expose_password_hash(env):
    active(env)
    identity = env[3]
    identity.update_profile("Tên mới", "en", "https://example.invalid/avatar.png")
    profile = identity.profile()
    assert profile["name"] == "Tên mới" and profile["language"] == "en"
    assert "password_hash" not in profile
    with pytest.raises(IdentityError):
        identity.update_profile("X", "vi")
    with pytest.raises(IdentityError):
        identity.update_profile("Name", "vi", "javascript:alert(1)")


def test_production_cannot_issue_dev_tokens_or_use_dev_activation(env):
    uid = active(env)
    repo, clock, auth, identity = env
    production = AuthService(repo, IdentityPolicy(app_env="production"), clock)
    with pytest.raises(IdentityError):
        production.request_reset("test@example.invalid")
    with pytest.raises(IdentityError):
        production.login("test@example.invalid", "TestPass123")
    assert (
        IdentityService(
            repo, identity.state, IdentityPolicy(app_env="production"), clock
        ).current_user()
        is None
    )


def test_admin_blocks_target_revokes_sessions_cannot_self_lock(env):
    uid = active(env)
    repo, clock, auth, target = env
    admin_id, tokens = auth.register(
        "Admin", "admin@example.invalid", "AdminPass123", 8, 18
    )
    auth.activate(tokens["verify"], "verify")
    repo.mutate(admin_id, lambda record: ({"role": "admin"}, None))
    admin = IdentityService(repo, {}, clock=clock)
    admin.login(auth.login("admin@example.invalid", "AdminPass123"))
    with pytest.raises(IdentityError):
        admin.set_blocked(admin_id, True)
    admin.set_blocked(uid, True)
    assert target.current_user() is None
    with pytest.raises(IdentityError):
        auth.login("test@example.invalid", "TestPass123")
    admin.set_blocked(uid, False)
    assert auth.login("test@example.invalid", "TestPass123")
