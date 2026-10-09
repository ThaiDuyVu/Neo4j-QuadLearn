"""Read-only graph filtering and DOT rendering; no fixed list of shapes."""
import json


def focus_graph(graph, shape_id=None, direction="both", depth=2):
    """Lọc đường đi có giới hạn; giữ cạnh trực tiếp gốc, không tạo cạnh bắc cầu."""
    if shape_id is None:
        return graph
    if direction not in {"parents", "children", "both"} or not 1 <= depth <= 8:
        raise ValueError("Hướng hoặc số bước quan hệ không hợp lệ.")
    nodes = {node["id"]: node for node in graph["nodes"]}
    if shape_id not in nodes:
        raise ValueError("Hình không còn tồn tại. Hãy làm mới dữ liệu.")
    visited, frontier = {shape_id}, {shape_id}
    for _ in range(depth):
        following = set()
        for edge in graph["edges"]:
            if direction in {"parents", "both"} and edge["source"] in frontier:
                following.add(edge["target"])
            if direction in {"children", "both"} and edge["target"] in frontier:
                following.add(edge["source"])
        frontier = (following & nodes.keys()) - visited
        visited.update(frontier)
        if not frontier:
            break
    return {
        "nodes": [node for node in graph["nodes"] if node["id"] in visited],
        "edges": [edge for edge in graph["edges"]
                  if edge["source"] in visited and edge["target"] in visited],
    }


def graph_dot(graph, selected=None, orientation="BT"):
    if orientation not in {"BT", "LR"}:
        raise ValueError("Bố cục không hợp lệ.")
    quote = lambda value: json.dumps(str(value), ensure_ascii=False)
    lines = ["digraph Geometry {", f"rankdir={orientation};",
             'graph [bgcolor="transparent", nodesep="0.45", ranksep="0.65"];',
             'node [shape=box, style="rounded,filled", fontname="Arial", fontsize=16, margin="0.20,0.12", color="#94a3b8", fillcolor="#f1f5f9", fontcolor="#0f172a"];',
             'edge [fontname="Arial", fontsize=11, color="#64748b", fontcolor="#475569", arrowsize=0.8];']
    for node in graph["nodes"]:
        emphasis = ', fillcolor="#2563eb", color="#1d4ed8", fontcolor="white"' if node["id"] == selected else ""
        lines.append(f'{quote(node["id"])} [label={quote(node["name"])}, tooltip={quote(node["id"])}{emphasis}];')
    for edge in graph["edges"]:
        lines.append(f'{quote(edge["source"])} -> {quote(edge["target"])} [label={quote(edge["type"])}];')
    return "\n".join(lines + ["}"])
