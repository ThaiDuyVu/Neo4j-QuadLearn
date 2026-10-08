# ==================================================
# DOMAIN OWNER: VU
# FEATURE: identity_learning_path
# Thành viên thêm page của domain vào PAGES tại đây.
# Không triển khai logic của các domain khác.
# ==================================================
from app.shared.contracts.navigation import PageSpec
from .pages.overview import render
PAGES = [PageSpec("Identity & Learning Path", "identity", render)]
