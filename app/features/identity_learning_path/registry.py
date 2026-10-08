# DOMAIN OWNER: VU. Thêm page chỉ sửa registry này, không sửa main/navigation.
from app.shared.contracts.navigation import PageSpec
from .pages import overview, account, path, profile, admin

PAGES = [
    PageSpec("Identity & Learning Path", "identity", overview.render),
    PageSpec("Tài khoản · Vũ", "identity-account", account.render),
    PageSpec("Lộ trình học · Vũ", "identity-path", path.render),
    PageSpec("Hồ sơ và cấp độ · Vũ", "identity-profile", profile.render),
    PageSpec("Quản lý người dùng · Vũ", "identity-admin", admin.render),
]
