"""Cấu hình local; không ghi mật khẩu vào log."""
from dataclasses import dataclass, field
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Settings:
    uri: str
    user: str
    password: str = field(repr=False)
    database: str = "neo4j"
    app_env: str = "development"

    @classmethod
    def load(cls):
        load_dotenv(ROOT / ".env", override=False)
        password = os.getenv("NEO4J_PASSWORD", "")
        if not password or len(password) < 8:
            raise ValueError("Đặt NEO4J_PASSWORD ít nhất 8 ký tự trong .env.")
        user = os.getenv("NEO4J_USER", "neo4j")
        if user != "neo4j":
            raise ValueError("Skeleton Docker Community khởi tạo user neo4j; dùng NEO4J_USER=neo4j.")
        return cls(os.getenv("NEO4J_URI", "bolt://localhost:7687"), user, password,
                   os.getenv("NEO4J_DATABASE", "neo4j"), os.getenv("APP_ENV", "development"))
