# ==================================================
# DOMAIN OWNER: DAT
# FEATURE: assessment_ai
# Thành viên thêm page của domain vào PAGES tại đây.
# Không triển khai logic của các domain khác.
# ==================================================
from app.shared.contracts.navigation import PageSpec
from .pages.overview import render
PAGES = [PageSpec("Assessment & AI", "assessment", render)]
