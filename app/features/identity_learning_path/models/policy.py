from dataclasses import dataclass
import os


@dataclass(frozen=True)
class IdentityPolicy:
    session_days: int = 7
    completion_threshold: float = 70.0
    score_threshold: float = 6.0
    average_policy: str = "all"
    allow_skip: bool = True
    app_env: str = "development"

    def __post_init__(self):
        if not 1 <= self.session_days <= 30:
            raise ValueError("VU_SESSION_DAYS phải từ 1 đến 30")
        if (
            not 0 <= self.completion_threshold <= 100
            or not 0 <= self.score_threshold <= 10
        ):
            raise ValueError("Ngưỡng mở khóa không hợp lệ")
        if self.average_policy not in ("all", "latest"):
            raise ValueError("VU_AVERAGE_POLICY phải là all hoặc latest")

    @classmethod
    def load(cls):
        return cls(
            int(os.getenv("VU_SESSION_DAYS", "7")),
            float(os.getenv("VU_UNLOCK_COMPLETION", "70")),
            float(os.getenv("VU_UNLOCK_SCORE", "6")),
            os.getenv("VU_AVERAGE_POLICY", "all"),
            os.getenv("VU_ALLOW_SKIP", "true").lower() == "true",
            os.getenv("APP_ENV", "development"),
        )
