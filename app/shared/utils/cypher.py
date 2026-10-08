"""Đọc scripts do nhóm quản lý, không dùng để parse Cypher tùy ý từ người dùng."""
from pathlib import Path

def statements(path: Path) -> list[str]:
    # Quy ước scripts: mỗi câu kết thúc bằng dòng riêng chỉ có dấu ;.
    chunks = path.read_text(encoding="utf-8").split("\n;" )
    return [chunk.strip() for chunk in chunks if chunk.strip()]
