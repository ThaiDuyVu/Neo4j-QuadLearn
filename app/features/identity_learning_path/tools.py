"""CLI tạo admin local: python -m app.features.identity_learning_path.tools create-admin --email <email>.
Không nhận password qua argument/log. Không nâng role qua form đăng ký.
"""

import argparse
from getpass import getpass
from app.core.config import Settings
from app.core.database import Database
from .repositories.identity import IdentityRepository
from .services.auth import AuthService
from .models.policy import IdentityPolicy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["create-admin"])
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    settings = Settings.load()
    if settings.app_env != "development":
        parser.error("Chỉ dùng CLI này trong development.")
    password = getpass("Mật khẩu admin (>=8 ký tự, chữ và số): ")
    if password != getpass("Nhập lại mật khẩu: "):
        parser.error("Mật khẩu không khớp.")
    db = Database(settings)
    try:
        db.verify()
        repository = IdentityRepository(db)
        auth = AuthService(repository, IdentityPolicy.load())
        uid, tokens = auth.register("Admin local", args.email, password, 8, 18)
        auth.activate(tokens["verify"], "verify")
        repository.mutate(uid, lambda user: ({"role": "admin"}, None))
        print(
            "Đã tạo admin local. Đăng nhập bằng email/password vừa nhập; chưa xác minh email thật."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
