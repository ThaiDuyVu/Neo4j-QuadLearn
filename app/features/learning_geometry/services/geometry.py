# DOMAIN OWNER: SON · learning_geometry
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
"""Ví dụ hình chữ nhật đúng ràng buộc; chưa phải bảng kéo thả."""
def rectangle(width: float, height: float) -> tuple[list[tuple[float, float]], float, float]:
    if width <= 0 or height <= 0:
        raise ValueError("Kích thước phải dương")
    return [(0, 0), (width, 0), (width, height), (0, height)], width*height, 2*(width+height)
