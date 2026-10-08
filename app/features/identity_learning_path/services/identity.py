# DOMAIN OWNER: VU · identity_learning_path
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
class IdentityService:
    def __init__(self, repository):
        self.repository = repository

    def current_user(self):
        # TODO Vũ: thay bằng session đã xác thực; không coi ID cố định là AUTH.
        return self.repository.user_by_id("user:demo-student")
