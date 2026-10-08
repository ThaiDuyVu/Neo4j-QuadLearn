// 1. Tiên quyết nhiều cấp (tối đa 8 bước để giới hạn chi phí demo).
MATCH p=(:Lesson {id:'lesson:9:cyclic'})-[:REQUIRES*1..8]->(l:Lesson)
RETURN DISTINCT l.id AS lesson, l.title_vi AS title, length(p) AS depth ORDER BY depth
;
// 2. Quan hệ phân loại; hình vuông thuộc cả chữ nhật và thoi.
MATCH p=(:Quadrilateral {id:'shape:square'})-[:IS_A*1..5]->(q:Quadrilateral)
RETURN DISTINCT q.name_vi AS shape, length(p) AS depth ORDER BY depth
;
// 3. Kiến thức liên quan theo loại hình.
MATCH (l:Lesson)-[:ABOUT]->(q:Quadrilateral)<-[:IS_A*0..3]-(child:Quadrilateral)
RETURN l.id AS lesson, q.name_vi AS concept, collect(DISTINCT child.name_vi) AS related_shapes
;
// 4. Ôn tập: lần làm điểm thấp -> topic -> lesson -> tiên quyết chưa hoàn thành.
// Seed có điểm 10 nên kết quả rỗng là hợp lệ.
MATCH (u:User {id:'user:demo-student'})-[:ATTEMPTED]->(a:Attempt)-[:FOR_TOPIC]->(t:Topic)-[:HAS_LESSON]->(:Lesson)-[:REQUIRES*1..8]->(p:Lesson)
WHERE a.score < 5 AND NOT EXISTS { MATCH (u)-[:COMPLETED]->(p) }
RETURN DISTINCT p.id AS lesson, p.title_vi AS title
;
// 5. Ngữ cảnh AI: bài hiện tại, bài liên quan và tiên quyết; chỉ published.
MATCH (:Lesson {id:'lesson:8:rectangle'})-[:REQUIRES|RELATED_TO*0..3]->(l:Lesson)
WHERE l.status='published'
RETURN DISTINCT l.id AS source_id, l.content_vi AS context LIMIT 8
;
// 6. Tiếp tục bài học gần nhất.
MATCH (:User {id:'user:demo-student'})-[r:LEARNING]->(l:Lesson)
WHERE r.status='in_progress'
RETURN l.id AS lesson ORDER BY r.last_seen DESC LIMIT 1
;
