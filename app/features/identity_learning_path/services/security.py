"""CORE AUTH: Argon2id cho password; SHA-256 chỉ cho token ngẫu nhiên đủ entropy."""

import hashlib
import re
import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from ..models.errors import IdentityError

hasher = PasswordHasher()


def normalize_email(email: str) -> str:
    result = email.strip().lower()
    if len(result) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", result):
        raise IdentityError("Email không hợp lệ.")
    return result


def validate_password(password: str):
    if (
        not 8 <= len(password) <= 256
        or not any(c.isalpha() for c in password)
        or not any(c.isdigit() for c in password)
    ):
        raise IdentityError("Mật khẩu phải 8–256 ký tự, có chữ và số.")


def verify_password(encoded: str, password: str) -> bool:
    try:
        return hasher.verify(encoded, password)
    except (VerificationError, InvalidHashError):
        return False


def new_token() -> str:
    return secrets.token_urlsafe(32)


def digest(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()
