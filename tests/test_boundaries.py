"""Kiểm tra imports bằng AST; feature không phụ thuộc nội bộ feature khác."""
import ast
from pathlib import Path

def test_no_cross_feature_imports():
    for domain in Path("app/features").iterdir():
        if not domain.is_dir() or domain.name.startswith("_"): continue
        for path in domain.rglob("*.py"):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                modules = ([node.module] if isinstance(node, ast.ImportFrom) and node.module else
                           [x.name for x in node.names] if isinstance(node, ast.Import) else [])
                for module in modules:
                    if module.startswith("app.features."):
                        assert module.split(".")[2] == domain.name, str(path)

def test_shared_import_graph_has_no_cycles():
    paths = list(Path("app").rglob("*.py"))
    modules = {".".join(p.with_suffix("").parts).removesuffix(".__init__"): p for p in paths}
    edges = {m:set() for m in modules}
    for name, path in modules.items():
        base = name if path.name == "__init__.py" else name.rsplit(".",1)[0]
        for node in ast.walk(ast.parse(path.read_text())):
            targets = []
            if isinstance(node, ast.Import): targets = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                target = node.module or ""
                if node.level:
                    prefix = base.split(".")
                    if node.level > 1: prefix = prefix[:-(node.level-1)]
                    target = ".".join(prefix + ([target] if target else []))
                targets = [target] + [target+"."+alias.name for alias in node.names]
            for target in targets:
                if target in modules and target != name: edges[name].add(target)
    visited, active = set(), set()
    def visit(name):
        assert name not in active, f"Import cycle at {name}"
        if name in visited:return
        active.add(name)
        for target in edges[name]:visit(target)
        active.remove(name); visited.add(name)
    for name in edges: visit(name)
