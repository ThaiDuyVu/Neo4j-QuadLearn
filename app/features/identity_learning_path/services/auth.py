# DOMAIN OWNER: VU. CORE AUTH: validation, kích hoạt, lockout, token và password.
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from .security import (
    normalize_email,
    validate_password,
    hasher,
    verify_password,
    new_token,
    digest,
)
from ..models.errors import IdentityError
from ..models.policy import IdentityPolicy

LOGIN_ERROR = "Không đăng nhập được. Kiểm tra thông tin hoặc trạng thái tài khoản."


def utcnow():
    return datetime.now(timezone.utc)


class AuthService:
    def __init__(self, repository, policy=None, clock=utcnow):
        self.repository = repository
        self.policy = policy or IdentityPolicy.load()
        self.clock = clock

    def _development(self):
        if self.policy.app_env != "development":
            raise IdentityError(
                "Email provider chưa tích hợp; token thử nghiệm chỉ dùng ở development."
            )

    def _token(self, kind, ttl):
        raw = new_token()
        return raw, dict(
            id=f"token:{uuid4()}",
            hash=digest(raw),
            kind=kind,
            expires_at=self.clock() + ttl,
        )

    def register(self, name, email, password, grade, age, guardian_email=""):
        self._development()
        email = normalize_email(email)
        validate_password(password)
        if (
            grade not in (6, 7, 8, 9)
            or not isinstance(age, int)
            or not 10 <= age <= 100
        ):
            raise IdentityError("Lớp 6–9 và tuổi từ 10 đến 100 là bắt buộc.")
        name = name.strip()
        if not 2 <= len(name) <= 100:
            raise IdentityError("Họ tên phải 2–100 ký tự.")
        guardian_required = age < 16
        guardian = normalize_email(guardian_email) if guardian_required else ""
        if guardian_required and guardian == email:
            raise IdentityError("Email người giám hộ phải khác email học sinh.")
        uid = f"user:{uuid4()}"
        now = self.clock()
        fields = dict(
            id=uid,
            name=name,
            email=email,
            password_hash=hasher.hash(password),
            role="student",
            language="vi",
            starting_grade=grade,
            guardian_required=guardian_required,
            guardian_email=guardian,
            email_verified=False,
            guardian_consent=not guardian_required,
            status="pending",
            demo=False,
            created_at=now,
            auth_version=0,
            failed_logins=0,
            activation_channel="development",
        )
        raw, token = self._token("verify", timedelta(days=1))
        tokens = [token]
        delivery = {"verify": raw}
        if guardian_required:
            raw, token = self._token("guardian", timedelta(days=1))
            tokens.append(token)
            delivery["guardian"] = raw
        self.repository.create(fields, tokens)
        return uid, delivery

    def activate(self, raw, kind):
        self._development()
        if kind not in ("verify", "guardian"):
            raise IdentityError("Loại token không hợp lệ.")
        return self.repository.consume_token(digest(raw), kind, self.clock())

    def login(self, email, password):
        email = normalize_email(email)
        now = self.clock()

        def decide(user):
            if not user:
                return {}, None
            until = user.get("locked_until")
            if hasattr(until, "to_native"):
                until = until.to_native()
            if until and until > now:
                return {}, None
            if (
                user.get("status") != "active"
                or user.get("demo")
                or (
                    self.policy.app_env != "development"
                    and user.get("activation_channel") == "development"
                )
            ):
                return {}, None
            if not verify_password(user.get("password_hash", ""), password):
                # Sau timeout lock, bắt đầu đợt sai mới thay vì tiếp tục ở count=5.
                failures = 0 if until else user.get("failed_logins", 0)
                failures += 1
                return {
                    "failed_logins": failures,
                    "locked_until": now + timedelta(minutes=15)
                    if failures >= 5
                    else None,
                }, None
            updates = {"failed_logins": 0, "locked_until": None}
            if hasher.check_needs_rehash(user["password_hash"]):
                updates["password_hash"] = hasher.hash(password)
            return updates, (user["id"], user.get("auth_version", 0))

        result = self.repository.mutate(email, decide, by_email=True)
        if not result:
            raise IdentityError(LOGIN_ERROR)
        raw = new_token()
        self.repository.create_session(result[0], result[1], digest(raw), now)
        return raw

    def request_reset(self, email):
        self._development()
        raw, token = self._token("reset", timedelta(minutes=30))
        return (
            raw if self.repository.reset_token(normalize_email(email), token) else None
        )

    def reset_password(self, raw, password):
        self._development()
        validate_password(password)
        return self.repository.consume_token(
            digest(raw), "reset", self.clock(), hasher.hash(password)
        )

    def change_password(self, identity, old, new):
        user = identity.require_user()
        validate_password(new)

        def change(record):
            if (
                not record
                or record.get("status") != "active"
                or not verify_password(record.get("password_hash", ""), old)
            ):
                raise IdentityError(
                    "Mật khẩu hiện tại không đúng hoặc tài khoản không hoạt động."
                )
            return {
                "password_hash": hasher.hash(new),
                "auth_version": record.get("auth_version", 0) + 1,
            }, None

        self.repository.mutate(user.id, change)
        identity.logout()  # đổi auth_version vô hiệu mọi session trên các browser khác.
