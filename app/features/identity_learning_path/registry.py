# DOMAIN OWNER: VU. Thêm page chỉ sửa registry này, không sửa main/navigation.
from app.shared.contracts.navigation import PageSpec
from .pages import overview, account, path, profile, admin

PAGES = [
    PageSpec("Tiến độ học tập", "identity", overview.render),
    PageSpec("Tài khoản", "identity-account", account.render),
    PageSpec("Lộ trình học", "identity-path", path.render),
    PageSpec("Hồ sơ và cấp độ", "identity-profile", profile.render),
    PageSpec("Quản lý người dùng", "identity-admin", admin.render),
]
