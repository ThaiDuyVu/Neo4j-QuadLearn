MERGE (l:Level {id:'level:6'}) SET l.grade=6, l.name_vi='Nhận biết', l.demo=true
;
MATCH (l:Level {id:'level:6'}) MERGE (c:Chapter {id:'chapter:6:demo'}) SET c.name_vi='Nhận biết', c.grade=6, c.order=1, c.demo=true MERGE (l)-[:HAS_CHAPTER]->(c)
;
MERGE (l:Level {id:'level:7'}) SET l.grade=7, l.name_vi='Nền tảng', l.demo=true
;
MATCH (l:Level {id:'level:7'}) MERGE (c:Chapter {id:'chapter:7:demo'}) SET c.name_vi='Nền tảng', c.grade=7, c.order=1, c.demo=true MERGE (l)-[:HAS_CHAPTER]->(c)
;
MERGE (l:Level {id:'level:8'}) SET l.grade=8, l.name_vi='Tính chất và chứng minh', l.demo=true
;
MATCH (l:Level {id:'level:8'}) MERGE (c:Chapter {id:'chapter:8:demo'}) SET c.name_vi='Tính chất và chứng minh', c.grade=8, c.order=1, c.demo=true MERGE (l)-[:HAS_CHAPTER]->(c)
;
MERGE (l:Level {id:'level:9'}) SET l.grade=9, l.name_vi='Tứ giác nội tiếp', l.demo=true
;
MATCH (l:Level {id:'level:9'}) MERGE (c:Chapter {id:'chapter:9:demo'}) SET c.name_vi='Tứ giác nội tiếp', c.grade=9, c.order=1, c.demo=true MERGE (l)-[:HAS_CHAPTER]->(c)
;
MATCH (c:Chapter {id:'chapter:6:demo'}) MERGE (t:Topic {id:'topic:6:rectangle'}) SET t.code='RECTANGLE', t.grade=6, t.cognitive_level='understand', t.name_vi='Hình chữ nhật trực quan', t.status='published', t.order=1, t.demo=true MERGE (c)-[:HAS_TOPIC]->(t) MERGE (l:Lesson {id:'lesson:6:rectangle'}) SET l.title_vi='Hình chữ nhật trực quan', l.title_en='Rectangle', l.content_vi='Hình chữ nhật có bốn góc vuông. Diện tích bằng chiều dài nhân chiều rộng.', l.grade=6, l.order=1, l.status='published', l.demo=true MERGE (t)-[:HAS_LESSON]->(l)
;
MATCH (c:Chapter {id:'chapter:7:demo'}) MERGE (t:Topic {id:'topic:7:parallel'}) SET t.code='PARALLEL', t.grade=7, t.cognitive_level='understand', t.name_vi='Hai đường thẳng song song', t.status='published', t.order=1, t.demo=true MERGE (c)-[:HAS_TOPIC]->(t) MERGE (l:Lesson {id:'lesson:7:parallel'}) SET l.title_vi='Hai đường thẳng song song', l.title_en='Parallel lines', l.content_vi='Hai đường thẳng song song trong cùng mặt phẳng không có điểm chung.', l.grade=7, l.order=1, l.status='published', l.demo=true MERGE (t)-[:HAS_LESSON]->(l)
;
MATCH (c:Chapter {id:'chapter:8:demo'}) MERGE (t:Topic {id:'topic:8:parallelogram'}) SET t.code='PARALLELOGRAM', t.grade=8, t.cognitive_level='understand', t.name_vi='Hình bình hành', t.status='published', t.order=1, t.demo=true MERGE (c)-[:HAS_TOPIC]->(t) MERGE (l:Lesson {id:'lesson:8:parallelogram'}) SET l.title_vi='Hình bình hành', l.title_en='Parallelogram', l.content_vi='Hình bình hành là tứ giác có các cặp cạnh đối song song.', l.grade=8, l.order=1, l.status='published', l.demo=true MERGE (t)-[:HAS_LESSON]->(l)
;
MATCH (c:Chapter {id:'chapter:8:demo'}) MERGE (t:Topic {id:'topic:8:rectangle'}) SET t.code='RECTANGLE', t.grade=8, t.cognitive_level='understand', t.name_vi='Hình chữ nhật và tính chất', t.status='published', t.order=1, t.demo=true MERGE (c)-[:HAS_TOPIC]->(t) MERGE (l:Lesson {id:'lesson:8:rectangle'}) SET l.title_vi='Hình chữ nhật và tính chất', l.title_en='Rectangle properties', l.content_vi='Hình chữ nhật là hình bình hành có một góc vuông. Hai đường chéo bằng nhau.', l.grade=8, l.order=1, l.status='published', l.demo=true MERGE (t)-[:HAS_LESSON]->(l)
;
MATCH (c:Chapter {id:'chapter:9:demo'}) MERGE (t:Topic {id:'topic:9:cyclic'}) SET t.code='CYCLIC', t.grade=9, t.cognitive_level='understand', t.name_vi='Tứ giác nội tiếp', t.status='published', t.order=1, t.demo=true MERGE (c)-[:HAS_TOPIC]->(t) MERGE (l:Lesson {id:'lesson:9:cyclic'}) SET l.title_vi='Tứ giác nội tiếp', l.title_en='Cyclic quadrilateral', l.content_vi='Tứ giác nội tiếp có bốn đỉnh cùng nằm trên một đường tròn. Tổng hai góc đối bằng 180 độ.', l.grade=9, l.order=1, l.status='published', l.demo=true MERGE (t)-[:HAS_LESSON]->(l)
;
MATCH (a:Lesson {id:'lesson:8:parallelogram'}), (b:Lesson {id:'lesson:7:parallel'}) MERGE (a)-[:REQUIRES]->(b)
;
MATCH (a:Lesson {id:'lesson:7:parallel'}), (b:Lesson {id:'lesson:6:rectangle'}) MERGE (a)-[:REQUIRES]->(b)
;
MATCH (a:Lesson {id:'lesson:8:rectangle'}), (b:Lesson {id:'lesson:8:parallelogram'}) MERGE (a)-[:REQUIRES]->(b)
;
MATCH (a:Lesson {id:'lesson:9:cyclic'}), (b:Lesson {id:'lesson:8:rectangle'}) MERGE (a)-[:REQUIRES]->(b)
;
MATCH (a:Lesson {id:'lesson:8:rectangle'}), (b:Lesson {id:'lesson:6:rectangle'}) MERGE (a)-[:RELATED_TO]->(b)
;
MERGE (q:Quadrilateral {id:'shape:quadrilateral'}) SET q.name_vi='Tứ giác', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:parallelogram'}) SET q.name_vi='Hình bình hành', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:rectangle'}) SET q.name_vi='Hình chữ nhật', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:rhombus'}) SET q.name_vi='Hình thoi', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:square'}) SET q.name_vi='Hình vuông', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:trapezoid'}) SET q.name_vi='Hình thang', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:isosceles-trapezoid'}) SET q.name_vi='Hình thang cân', q.demo=true
;
MERGE (q:Quadrilateral {id:'shape:cyclic'}) SET q.name_vi='Tứ giác nội tiếp', q.demo=true
;
MATCH (a:Quadrilateral {id:'shape:square'}), (b:Quadrilateral {id:'shape:rectangle'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:square'}), (b:Quadrilateral {id:'shape:rhombus'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:rectangle'}), (b:Quadrilateral {id:'shape:parallelogram'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:rhombus'}), (b:Quadrilateral {id:'shape:parallelogram'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:parallelogram'}), (b:Quadrilateral {id:'shape:quadrilateral'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:trapezoid'}), (b:Quadrilateral {id:'shape:quadrilateral'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:isosceles-trapezoid'}), (b:Quadrilateral {id:'shape:trapezoid'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:cyclic'}), (b:Quadrilateral {id:'shape:quadrilateral'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (a:Quadrilateral {id:'shape:rectangle'}), (b:Quadrilateral {id:'shape:cyclic'}) MERGE (a)-[:IS_A]->(b)
;
MATCH (l:Lesson {id:'lesson:8:rectangle'}), (q:Quadrilateral {id:'shape:rectangle'}) MERGE (l)-[:ABOUT]->(q) MERGE (g:GeometryConfig {id:'geometry:rectangle'}) SET g.kind='rectangle', g.width=4.0, g.height=3.0, g.demo=true MERGE (l)-[:ILLUSTRATED_BY]->(g)
;
MATCH (l:Level {id:'level:8'}), (done:Lesson {id:'lesson:8:parallelogram'}), (next:Lesson {id:'lesson:8:rectangle'}) MERGE (u:User {id:'user:demo-student'}) SET u.name='Học sinh demo', u.email='student@example.invalid', u.role='student', u.language='vi', u.status='demo', u.demo=true MERGE (u)-[:STUDIES_AT]->(l) MERGE (u)-[c:COMPLETED]->(done) SET c.completed_at=datetime('2026-01-01T09:00:00Z') MERGE (u)-[s:LEARNING]->(next) SET s.status='in_progress', s.last_seen=datetime('2026-01-01T09:30:00Z') MERGE (p:Progress {id:'progress:demo:8'}) SET p.user_id=u.id, p.level_id=l.id, p.completion=50.0, p.average_score=10.0, p.unlocked=true, p.demo=true MERGE (u)-[:HAS_PROGRESS]->(p) MERGE (p)-[:FOR_LEVEL]->(l)
;
MATCH (t:Topic {id:'topic:8:rectangle'}) MERGE (q:Question {id:'question:8:rectangle:1'}) SET q.text_vi='Hình chữ nhật có bao nhiêu góc vuông?', q.grade=8, q.type='single', q.difficulty='recognize', q.explanation_vi='Cả bốn góc đều là góc vuông.', q.status='published', q.demo=true MERGE (t)-[:HAS_QUESTION]->(q) MERGE (o:Option {id:'option:rectangle:4'}) SET o.text_vi='4', o.correct=true, o.demo=true MERGE (q)-[:HAS_OPTION]->(o) MERGE (wrong:Option {id:'option:rectangle:2'}) SET wrong.text_vi='2', wrong.correct=false, wrong.demo=true MERGE (q)-[:HAS_OPTION]->(wrong)
;
MATCH (u:User {id:'user:demo-student'}), (t:Topic {id:'topic:8:rectangle'}), (q:Question {id:'question:8:rectangle:1'}), (o:Option {id:'option:rectangle:4'}) MERGE (a:Attempt {id:'attempt:demo:1'}) SET a.score=10.0, a.status='completed', a.started_at=datetime('2026-01-01T09:00:00Z'), a.finished_at=datetime('2026-01-01T09:02:00Z'), a.demo=true MERGE (u)-[:ATTEMPTED]->(a) MERGE (a)-[:FOR_TOPIC]->(t) MERGE (answer:AttemptAnswer {id:'answer:demo:1:1'}) SET answer.correct=true, answer.demo=true MERGE (a)-[:HAS_ANSWER]->(answer) MERGE (answer)-[:ANSWERS]->(q) MERGE (answer)-[:SELECTED]->(o)
;
MATCH (t:Topic {id:'topic:8:rectangle'}) MERGE (e:EssayProblem {id:'essay:8:rectangle:1'}) SET e.prompt_vi='Tính diện tích hình chữ nhật có chiều dài 4 cm, chiều rộng 3 cm.', e.assumptions_vi='a=4 cm, b=3 cm', e.conclusion_vi='Tính S', e.solution_vi='S=4×3=12 cm²', e.grade=8, e.demo=true MERGE (t)-[:HAS_ESSAY]->(e) MERGE (h:EssayHint {id:'hint:rectangle:1'}) SET h.order=1, h.text_vi='Dùng công thức S=a×b.', h.demo=true MERGE (e)-[:HAS_HINT]->(h)
;
MATCH (u:User {id:'user:demo-student'}), (l:Lesson {id:'lesson:8:rectangle'}) MERGE (s:ChatSession {id:'chat:demo:1'}) SET s.demo=true MERGE (u)-[:HAS_CHAT]->(s) MERGE (s)-[:CONTEXT_LESSON]->(l) MERGE (m:ChatMessage {id:'message:demo:1'}) SET m.role='assistant', m.content='MOCK: xem bài Hình chữ nhật.', m.provider='mock', m.created_at=datetime('2026-01-01T09:00:00Z'), m.demo=true MERGE (s)-[:HAS_MESSAGE]->(m)
;
