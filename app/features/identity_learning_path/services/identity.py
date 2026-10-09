# DOMAIN OWNER: VU. CORE SESSION: mọi module hỏi current_user qua contract này.
from datetime import timedelta
from .security import digest
from .auth import utcnow
from ..models.policy import IdentityPolicy
from ..models.errors import IdentityError


class IdentityService:
    def __init__(
        self, repository, session_state=None, policy=None, clock=utcnow, demo=False
    ):
        self.repository = repository
        self.state = session_state if session_state is not None else {}
        self.policy = policy or IdentityPolicy.load()
        self.clock = clock
        self.demo = demo

    def current_user(self):
        raw = self.state.get("vu_session")
        if raw:
            now = self.clock()
            user = self.repository.resolve_session(
                digest(raw),
                now,
                now - timedelta(days=self.policy.session_days),
                self.policy.app_env,
            )
            if user:
                return user
            self.state.pop("vu_session", None)
        if self.demo or self.state.get("vu_demo"):
            if self.policy.app_env == "development":
                return self.repository.user_by_id("user:demo-student")
        return None

    def login(self, token):
        self.state["vu_session"] = token
        self.state.pop("vu_demo", None)

    def logout(self):
        raw = self.state.pop("vu_session", None)
        if raw:
            self.repository.delete_session(digest(raw))
        self.state.pop("vu_demo", None)
        self.state.pop("vu_dev_delivery", None)

    def enter_demo(self):
        if self.policy.app_env != "development":
            raise IdentityError("Demo chỉ dùng ở development.")
        self.logout()
        self.state["vu_demo"] = True

    def require_user(self, user_id=None, admin=False):
        user = self.current_user()
        if not user or user.demo:
            raise IdentityError(
                "Vui lòng đăng nhập tài khoản đã kích hoạt; demo chỉ được đọc."
            )
        if user_id is not None and user.id != user_id:
            raise IdentityError("Không có quyền thao tác dữ liệu người dùng khác.")
        if admin and user.role != "admin":
            raise IdentityError("Chức năng chỉ dành cho admin.")
        return user

    def profile(self):
        user = self.require_user()
        profile = self.repository.profile(user.id)
        # Không trả password hash/token/internal counter cho UI.
        return {
            key: profile.get(key)
            for key in (
                "id",
                "name",
                "email",
                "grade",
                "language",
                "avatar_url",
                "guardian_required",
                "email_verified",
                "guardian_consent",
            )
        }

    def update_profile(self, name, language, avatar_url=""):
        user = self.require_user()
        name = name.strip()
        avatar_url = avatar_url.strip()
        if not 2 <= len(name) <= 100 or language not in ("vi", "en"):
            raise IdentityError("Tên 2–100 ký tự; ngôn ngữ vi/en.")
        if avatar_url and (
            len(avatar_url) > 2048 or not avatar_url.startswith(("https://", "http://"))
        ):
            raise IdentityError("Ảnh đại diện phải là URL http/https hợp lệ.")

        def update(record):
            if not record or record.get("status") != "active":
                raise IdentityError("Tài khoản không hoạt động.")
            return dict(name=name, language=language, avatar_url=avatar_url), None

        self.repository.mutate(user.id, update)

    def search_users(self, term=""):
        self.require_user(admin=True)
        return self.repository.users(term)

    def set_blocked(self, user_id, blocked):
        actor = self.require_user(admin=True)
        if user_id == actor.id:
            raise IdentityError("Không được tự khóa tài khoản admin đang dùng.")

        def change(record):
            if not record:
                raise IdentityError("Không tìm thấy người dùng.")
            if record.get("demo"):
                raise IdentityError("Không sửa fixture demo qua admin.")
            active = record.get("email_verified") and (
                not record.get("guardian_required") or record.get("guardian_consent")
            )
            return {
                "status": "blocked" if blocked else ("active" if active else "pending"),
                "auth_version": record.get("auth_version", 0) + 1,
                "failed_logins": 0,
                "locked_until": None,
            }, None

        self.repository.mutate(user_id, change)
