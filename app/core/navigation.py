"""Tự tìm registry trong mỗi feature; thêm page không phải sửa main.py."""
from importlib import import_module
import pkgutil
import app.features

def discover_pages():
    pages = []
    for feature in sorted(pkgutil.iter_modules(app.features.__path__), key=lambda item: item.name):
        if feature.ispkg:
            registry = import_module(f"app.features.{feature.name}.registry")
            pages.extend(registry.PAGES)
    paths = [page.path for page in pages]
    if len(paths) != len(set(paths)):
        raise ValueError("Feature registry có url_path trùng nhau")
    return pages
