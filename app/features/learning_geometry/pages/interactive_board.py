# DOMAIN OWNER: SON · learning_geometry
# Component bảng hình: giữ giao diện HTML/JS độc lập với truy vấn và nội dung bài học.
import streamlit.components.v1 as components


def render_geometry_board(shape_type: str):
    interactive_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 2px; box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; background: #ffffff; color: #0f172a; }}
            #canvas {{ width: 100%; height: auto; display: block; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; touch-action: none; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }}
            
            .detected-badge {{ margin-top: 12px; padding: 8px 24px; border-radius: 20px; font-size: 18px; font-weight: 800; background: #eff6ff; color: #1d4ed8; border: 2px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            
            .properties-panel {{ margin-top: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #2563eb; padding: 12px 20px; border-radius: 8px; max-width: 760px; width: 90%; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            .properties-title {{ font-weight: 700; color: #0f172a; margin-bottom: 6px; font-size: 15px; display: flex; align-items: center; gap: 6px; }}
            .properties-list {{ margin: 0; padding-left: 20px; color: #334155; font-size: 14px; line-height: 1.5; }}
            
            .control-panel {{ display: flex; gap: 16px; margin-top: 10px; flex-wrap: wrap; justify-content: center; background: #ffffff; padding: 10px 18px; border-radius: 10px; border: 1px solid #cbd5e1; }}
            .input-group {{ display: flex; align-items: center; gap: 8px; font-weight: 600; color: #334155; font-size: 14px; }}
            .input-group input {{ width: 65px; padding: 5px 8px; border: 1px solid #94a3b8; border-radius: 6px; font-weight: 700; color: #2563eb; font-size: 14px; text-align: center; }}
            
            .info-panel {{ display: flex; gap: 16px; margin-top: 10px; flex-wrap: wrap; justify-content: center; }}
            .metric {{ background: #f1f5f9; padding: 8px 18px; border-radius: 8px; font-size: 15px; font-weight: 600; color: #1e293b; border: 1px solid #e2e8f0; }}
            .metric span {{ color: #2563eb; font-weight: 700; font-size: 16px; }}
            
            .edge-label {{ font-size: 14px; font-weight: bold; fill: #2563eb; text-anchor: middle; dominant-baseline: middle; }}
            .angle-label {{ font-size: 13px; font-weight: 700; fill: #d97706; text-anchor: middle; }}
            * {{ box-sizing: border-box; }}
            .workspace {{ display: grid; grid-template-columns: minmax(0, 1.8fr) minmax(250px, 1fr); gap: 20px; align-items: start; }}
            .drawing-panel {{ min-width: 0; background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; }}
            .settings-panel {{ padding: 18px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; }}
            h3 {{ margin: 0 0 8px; font-size: 16px; }}
            .helper {{ margin: 0 0 16px; font-size: 13px; line-height: 1.6; color: #64748b; }}
            .detected-badge {{ font-size: 15px; padding: 10px 12px; text-align: center; box-shadow: none; }}
            .info-panel {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 16px; }}
            .metric {{ font-size: 13px; text-align: center; padding: 12px 8px; }}
            .metric span {{ display: block; margin-top: 6px; font-size: 22px; }}
            .control-panel {{ padding: 0; margin: 0; border: 0; background: none; display: grid; gap: 14px; }}
            .input-group {{ justify-content: space-between; gap: 12px; }}
            .input-group input {{ width: 90px; padding: 8px; }}
            .properties-panel {{ width: 100%; margin-top: 24px; padding: 14px; box-shadow: none; }}
            @media (max-width: 720px) {{
                .workspace {{ grid-template-columns: 1fr; gap: 12px; }}
                .drawing-panel, .settings-panel {{ padding: 12px; }}
            }}
        </style>
    </head>
    <body>
        <div class="workspace">
            <section class="drawing-panel" aria-label="Hình vẽ tương tác">
                <h3>Hình vẽ tương tác</h3>
                <p class="helper">Kéo một đỉnh để quan sát sự thay đổi của cạnh, góc và diện tích.</p>
        <svg id="canvas" width="800" height="340" viewBox="0 0 800 340">
            <polygon id="poly" fill="#3b82f618" stroke="#2563eb" stroke-width="3"/>

            <text id="lblAB" class="edge-label"></text>
            <text id="lblBC" class="edge-label"></text>
            <text id="lblCD" class="edge-label"></text>
            <text id="lblDA" class="edge-label"></text>

            <text id="angA" class="angle-label"></text>
            <text id="angB" class="angle-label"></text>
            <text id="angC" class="angle-label"></text>
            <text id="angD" class="angle-label"></text>

            <circle id="ptA" r="10" fill="#ef4444" stroke="#ffffff" stroke-width="3" style="cursor: pointer;"/>
            <circle id="ptB" r="10" fill="#ef4444" stroke="#ffffff" stroke-width="3" style="cursor: pointer;"/>
            <circle id="ptC" r="10" fill="#ef4444" stroke="#ffffff" stroke-width="3" style="cursor: pointer;"/>
            <circle id="ptD" r="10" fill="#ef4444" stroke="#ffffff" stroke-width="3" style="cursor: pointer;"/>

            <text id="lblA" font-weight="bold" fill="#0f172a" font-size="16">A</text>
            <text id="lblB" font-weight="bold" fill="#0f172a" font-size="16">B</text>
            <text id="lblC" font-weight="bold" fill="#0f172a" font-size="16">C</text>
            <text id="lblD" font-weight="bold" fill="#0f172a" font-size="16">D</text>
        </svg>


                <div class="detected-badge" id="shapeTypeResult">Đang nhận diện...</div>
                <div class="info-panel">
                    <div class="metric">Chu vi · unit <span id="valP">0</span></div>
                    <div class="metric">Diện tích · unit² <span id="valS">0</span></div>
                </div>
            </section>
            <aside class="settings-panel" aria-label="Thông số và tính chất">
                <h3>Thông số hình</h3>
                <p class="helper">Nhập kích thước để dựng lại hình ban đầu. Kéo đỉnh sẽ thay đổi hình tự do.</p>
                <div class="control-panel" id="controls"></div>
                <div class="properties-panel">
                    <div class="properties-title">Tính chất hình đang vẽ</div>
                    <ul class="properties-list" id="propList"><li>Đang cập nhật...</li></ul>
                </div>
            </aside>
        </div>

        <script>
            const mode = "{shape_type}";
            let pts = [
                {{x: 220, y: 50}},   // A
                {{x: 580, y: 50}},   // B
                {{x: 580, y: 270}},  // C
                {{x: 220, y: 270}}   // D
            ];

            const controlsDiv = document.getElementById("controls");

            if (mode === "Hình vuông") {{
                controlsDiv.innerHTML = `<div class="input-group">Cạnh (a): <input type="number" id="inpA" value="11" min="1" max="20" step="0.5"></div>`;
            }} else if (mode === "Hình chữ nhật") {{
                controlsDiv.innerHTML = `
                    <div class="input-group">Chiều dài (a): <input type="number" id="inpA" value="13" min="1" max="20" step="0.5"></div>
                    <div class="input-group">Chiều rộng (b): <input type="number" id="inpB" value="8" min="1" max="20" step="0.5"></div>
                `;
            }} else if (mode === "Hình bình hành") {{
                controlsDiv.innerHTML = `
                    <div class="input-group">Đáy (a): <input type="number" id="inpA" value="13" min="1" max="20" step="0.5"></div>
                    <div class="input-group">Cạnh bên (b): <input type="number" id="inpB" value="8" min="1" max="20" step="0.5"></div>
                    <div class="input-group">Góc (α°): <input type="number" id="inpAng" value="60" min="20" max="160"></div>
                `;
            }} else if (mode === "Hình thoi") {{
                controlsDiv.innerHTML = `
                    <div class="input-group">Cạnh (a): <input type="number" id="inpA" value="10" min="1" max="20" step="0.5"></div>
                    <div class="input-group">Góc nhọn (α°): <input type="number" id="inpAng" value="60" min="20" max="160"></div>
                `;
            }} else if (mode === "Hình thang cân") {{
                controlsDiv.innerHTML = `
                    <div class="input-group">Đáy nhỏ (a): <input type="number" id="inpA" value="8" min="1" max="20" step="0.5"></div>
                    <div class="input-group">Đáy lớn (b): <input type="number" id="inpB" value="14" min="1" max="25" step="0.5"></div>
                    <div class="input-group">Góc đáy (α°): <input type="number" id="inpAng" value="65" min="30" max="85"></div>
                `;
            }}

            document.querySelectorAll("#controls input").forEach(input => {{
                input.addEventListener("input", rebuildShapeFromInputs);
            }});

            function rebuildShapeFromInputs() {{
                const scale = 28;
                const cx = 400, cy = 160;

                if (mode === "Hình vuông") {{
                    const a = parseFloat(document.getElementById("inpA").value) || 10;
                    const w = a * scale;
                    pts = [
                        {{x: cx - w/2, y: cy - w/2}},
                        {{x: cx + w/2, y: cy - w/2}},
                        {{x: cx + w/2, y: cy + w/2}},
                        {{x: cx - w/2, y: cy + w/2}}
                    ];
                }} else if (mode === "Hình chữ nhật") {{
                    const a = parseFloat(document.getElementById("inpA").value) || 12;
                    const b = parseFloat(document.getElementById("inpB").value) || 7;
                    const w = a * scale, h = b * scale;
                    pts = [
                        {{x: cx - w/2, y: cy - h/2}},
                        {{x: cx + w/2, y: cy - h/2}},
                        {{x: cx + w/2, y: cy + h/2}},
                        {{x: cx - w/2, y: cy + h/2}}
                    ];
                }} else if (mode === "Hình bình hành") {{
                    const a = parseFloat(document.getElementById("inpA").value) || 12;
                    const b = parseFloat(document.getElementById("inpB").value) || 7;
                    const ang = (parseFloat(document.getElementById("inpAng").value) || 60) * Math.PI / 180;
                    const w = a * scale, h = b * Math.sin(ang) * scale, dx = b * Math.cos(ang) * scale;
                    pts = [
                        {{x: cx - w/2 + dx, y: cy - h/2}},
                        {{x: cx + w/2 + dx, y: cy - h/2}},
                        {{x: cx + w/2, y: cy + h/2}},
                        {{x: cx - w/2, y: cy + h/2}}
                    ];
                }} else if (mode === "Hình thoi") {{
                    const a = parseFloat(document.getElementById("inpA").value) || 10;
                    const ang = (parseFloat(document.getElementById("inpAng").value) || 60) * Math.PI / 180;
                    const w = a * scale, h = a * Math.sin(ang) * scale, dx = a * Math.cos(ang) * scale;
                    pts = [
                        {{x: cx - w/2 + dx, y: cy - h/2}},
                        {{x: cx + w/2 + dx, y: cy - h/2}},
                        {{x: cx + w/2, y: cy + h/2}},
                        {{x: cx - w/2, y: cy + h/2}}
                    ];
                }} else if (mode === "Hình thang cân") {{
                    const a = parseFloat(document.getElementById("inpA").value) || 8;
                    const b = parseFloat(document.getElementById("inpB").value) || 14;
                    const ang = (parseFloat(document.getElementById("inpAng").value) || 65) * Math.PI / 180;
                    const dx = ((b - a) / 2) * scale;
                    const h = ((b - a) / 2) * Math.tan(ang) * scale;
                    const wA = a * scale, wB = b * scale;
                    pts = [
                        {{x: cx - wA/2, y: cy - h/2}},
                        {{x: cx + wA/2, y: cy - h/2}},
                        {{x: cx + wB/2, y: cy + h/2}},
                        {{x: cx - wB/2, y: cy + h/2}}
                    ];
                }}
                // Giữ hình và nhãn nằm trong khung, kể cả khi nhập kích thước lớn.
                const minX = Math.min(0, ...pts.map(p => p.x - 40));
                const minY = Math.min(0, ...pts.map(p => p.y - 40));
                const maxX = Math.max(800, ...pts.map(p => p.x + 40));
                const maxY = Math.max(340, ...pts.map(p => p.y + 40));
                svg.setAttribute("viewBox", `${{minX}} ${{minY}} ${{maxX-minX}} ${{maxY-minY}}`);
                updateUI();
            }}

            let selectedPt = -1;
            const svg = document.getElementById("canvas");

            function dist(p1, p2) {{ return Math.hypot(p2.x - p1.x, p2.y - p1.y); }}

            function calcAngle(p1, p2, p3) {{
                const v1 = {{x: p1.x - p2.x, y: p1.y - p2.y}};
                const v2 = {{x: p3.x - p2.x, y: p3.y - p2.y}};
                const dot = v1.x * v2.x + v1.y * v2.y;
                const m1 = Math.hypot(v1.x, v1.y), m2 = Math.hypot(v2.x, v2.y);
                if (m1 === 0 || m2 === 0) return 0;
                let cosTheta = dot / (m1 * m2);
                return Math.round(Math.acos(Math.max(-1, Math.min(1, cosTheta))) * (180 / Math.PI));
            }}

            // Phân loại hình & Trả về danh sách tính chất
            function classifyShape(pts, angles, edgeLens) {{
                const [AB, BC, CD, DA] = edgeLens;
                const [angA, angB, angC, angD] = angles;
                const tol = 0.05;  // Sai số độ dài theo unit, không phải pixel.

                const eq = (x, y) => Math.abs(x - y) <= tol;
                const is90 = (a) => Math.abs(a - 90) <= 1.2;

                const parallel = (a, b, c, d) => {{
                    const ux = b.x-a.x, uy = b.y-a.y, vx = d.x-c.x, vy = d.y-c.y;
                    const norm = Math.hypot(ux, uy) * Math.hypot(vx, vy);
                    return norm > 0 && Math.abs(ux*vy-uy*vx) / norm <= 0.01;
                }};
                const par1 = parallel(pts[0], pts[1], pts[3], pts[2]);
                const par2 = parallel(pts[0], pts[3], pts[1], pts[2]);

                const all90 = is90(angA) && is90(angB) && is90(angC) && is90(angD);
                const allEqual = eq(AB, BC) && eq(BC, CD) && eq(CD, DA);
                const oppEqual = eq(AB, CD) && eq(BC, DA);

                if (all90 && allEqual) {{
                    return {{
                        name: "Hình vuông 🟦",
                        props: [
                            "Bốn cạnh bằng nhau: AB = BC = CD = DA",
                            "Bốn góc vuông bằng nhau = 90°",
                            "Hai đường chéo bằng nhau, vuông góc tại trung điểm mỗi đường",
                            "Vừa là hình chữ nhật, vừa là hình thoi đặc biệt"
                        ]
                    }};
                }}
                if (all90) {{
                    return {{
                        name: "Hình chữ nhật 🟧",
                        props: [
                            "Bốn góc đều bằng nhau = 90°",
                            "Các cạnh đối bằng nhau và song song: AB = CD, AD = BC",
                            "Hai đường chéo bằng nhau và cắt nhau tại trung điểm mỗi đường"
                        ]
                    }};
                }}
                if (allEqual) {{
                    return {{
                        name: "Hình thoi 🟪",
                        props: [
                            "Bốn cạnh bằng nhau: AB = BC = CD = DA",
                            "Các góc đối bằng nhau: ∠A = ∠C, ∠B = ∠D",
                            "Hai đường chéo vuông góc với nhau tại trung điểm mỗi đường",
                            "Hai đường chéo là đường phân giác của các góc"
                        ]
                    }};
                }}
                if (oppEqual || (par1 && par2)) {{
                    return {{
                        name: "Hình bình hành 🟩",
                        props: [
                            "Các cạnh đối song song và bằng nhau: AB ∥ CD, AD ∥ BC",
                            "Các góc đối bằng nhau: ∠A = ∠C, ∠B = ∠D",
                            "Hai đường chéo cắt nhau tại trung điểm của mỗi đường"
                        ]
                    }};
                }}
                if (par1 && eq(DA, BC)) {{
                    return {{
                        name: "Hình thang cân 🟨",
                        props: [
                            "Hai đáy song song với nhau: AB ∥ CD",
                            "Hai cạnh bên bằng nhau: AD = BC",
                            "Hai góc kề một đáy bằng nhau: ∠D = ∠C, ∠A = ∠B",
                            "Hai đường chéo bằng nhau: AC = BD"
                        ]
                    }};
                }}
                if (par1 || par2) {{
                    return {{
                        name: "Hình thang 📐",
                        props: [
                            "Có một cặp cạnh đối song song với nhau (hai đáy)",
                            "Tổng hai góc kề một cạnh bên bằng 180°"
                        ]
                    }};
                }}
                return {{
                    name: "Tứ giác thường 🔷",
                    props: [
                        "Tổng bốn góc trong bằng 360°",
                        "Không có cặp cạnh đối nào bằng nhau hoặc song song đặc biệt"
                    ]
                }};
            }}

            function updateUI() {{
                const poly = document.getElementById("poly");
                poly.setAttribute("points", pts.map(p => `${{p.x}},${{p.y}}`).join(" "));

                const names = ["A", "B", "C", "D"];
                names.forEach((lbl, i) => {{
                    const circle = document.getElementById("pt" + lbl);
                    const text = document.getElementById("lbl" + lbl);
                    circle.setAttribute("cx", pts[i].x);
                    circle.setAttribute("cy", pts[i].y);
                    
                    const cx = (pts[0].x + pts[1].x + pts[2].x + pts[3].x) / 4;
                    const cy = (pts[0].y + pts[1].y + pts[2].y + pts[3].y) / 4;
                    const dx = pts[i].x - cx, dy = pts[i].y - cy;
                    const len = Math.hypot(dx, dy) || 1;
                    
                    text.setAttribute("x", pts[i].x + (dx / len) * 22 - 6);
                    text.setAttribute("y", pts[i].y + (dy / len) * 22 + 6);
                }});

                const edgeLens = [
                    dist(pts[0], pts[1]) / 28,
                    dist(pts[1], pts[2]) / 28,
                    dist(pts[2], pts[3]) / 28,
                    dist(pts[3], pts[0]) / 28
                ];

                const edges = [
                    {{ id: "lblAB", p1: pts[0], p2: pts[1], len: edgeLens[0] }},
                    {{ id: "lblBC", p1: pts[1], p2: pts[2], len: edgeLens[1] }},
                    {{ id: "lblCD", p1: pts[2], p2: pts[3], len: edgeLens[2] }},
                    {{ id: "lblDA", p1: pts[3], p2: pts[0], len: edgeLens[3] }}
                ];

                edges.forEach(e => {{
                    const el = document.getElementById(e.id);
                    const mx = (e.p1.x + e.p2.x) / 2, my = (e.p1.y + e.p2.y) / 2;
                    el.setAttribute("x", mx);
                    el.setAttribute("y", my - 10);
                    el.textContent = e.len.toFixed(1);
                }});

                const anglesVals = [
                    calcAngle(pts[3], pts[0], pts[1]),
                    calcAngle(pts[0], pts[1], pts[2]),
                    calcAngle(pts[1], pts[2], pts[3]),
                    calcAngle(pts[2], pts[3], pts[0])
                ];

                const angles = [
                    {{ id: "angA", val: anglesVals[0], p: pts[0] }},
                    {{ id: "angB", val: anglesVals[1], p: pts[1] }},
                    {{ id: "angC", val: anglesVals[2], p: pts[2] }},
                    {{ id: "angD", val: anglesVals[3], p: pts[3] }}
                ];

                angles.forEach(a => {{
                    const el = document.getElementById(a.id);
                    el.setAttribute("x", a.p.x);
                    el.setAttribute("y", a.p.y + 22);
                    el.textContent = a.val + "°";
                }});

                // Nhận diện loại hình & Cập nhật danh sách tính chất
                const shapeInfo = classifyShape(pts, anglesVals, edgeLens);
                document.getElementById("shapeTypeResult").innerText = "Hình dạng nhận diện: " + shapeInfo.name;
                
                const propListEl = document.getElementById("propList");
                propListEl.innerHTML = shapeInfo.props.map(p => `<li>${{p}}</li>`).join("");

                let p = 0;
                for (let i = 0; i < 4; i++) p += dist(pts[i], pts[(i + 1) % 4]);
                
                let s = Math.abs(
                    (pts[0].x*(pts[1].y - pts[3].y) + 
                     pts[1].x*(pts[2].y - pts[0].y) + 
                     pts[2].x*(pts[3].y - pts[1].y) + 
                     pts[3].x*(pts[0].y - pts[2].y)) / 2
                );

                document.getElementById("valP").innerText = (p / 28).toFixed(1);
                document.getElementById("valS").innerText = (s / (28*28)).toFixed(1);
            }}

            function getMousePos(e) {{
                // Chuyển tọa độ màn hình sang viewBox khi canvas co theo khu vực hiển thị.
                const point = svg.createSVGPoint();
                point.x = e.clientX;
                point.y = e.clientY;
                const pos = point.matrixTransform(svg.getScreenCTM().inverse());
                return {{
                    x: Math.max(svg.viewBox.baseVal.x + 20, Math.min(svg.viewBox.baseVal.x + svg.viewBox.baseVal.width - 20, pos.x)),
                    y: Math.max(svg.viewBox.baseVal.y + 20, Math.min(svg.viewBox.baseVal.y + svg.viewBox.baseVal.height - 20, pos.y))
                }};
            }}

            svg.addEventListener("mousedown", (e) => {{
                const pos = getMousePos(e);
                pts.forEach((p, i) => {{
                    if (Math.hypot(p.x - pos.x, p.y - pos.y) < 20) selectedPt = i;
                }});
            }});

            svg.addEventListener("mousemove", (e) => {{
                if (selectedPt !== -1) {{
                    const pos = getMousePos(e);
                    pts[selectedPt] = pos;
                    updateUI();
                }}
            }});

            window.addEventListener("mouseup", () => selectedPt = -1);

            rebuildShapeFromInputs();
        </script>
    </body>
    </html>
    '''

    components.html(interactive_html, height=720, scrolling=True)
