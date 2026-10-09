# Neo4j Graph Schema

## Node và thuộc tính

| Node | Owner ghi | ID / thuộc tính chính |
|---|---|---|
| User | Vũ | user:<uuid>; email unique, name, role student/admin, language, status; password_hash/consent TODO |
| Level | Sơn (catalog dùng chung) | level:6…9; grade unique, name_vi |
| Chapter | Sơn | chapter:<grade>:<slug>; grade, name_vi/en, order |
| Topic | Sơn | topic:<grade>:<slug>; code, grade, cognitive_level, name_vi/en, status, order |
| Lesson | Sơn | lesson:<grade>:<slug>; title_vi/en, content_vi/en, grade, order, status |
| Quadrilateral | Sơn | shape:<slug>; name_vi/en; taxonomy không phụ thuộc lớp |
| GeometryConfig | Sơn | geometry:<uuid/slug>; kind, width/height hoặc config_json cho dữ liệu renderer |
| Question | Đạt | question:<uuid>; grade, difficulty, type, text_vi/en, explanation_vi/en, status |
| Option | Đạt | option:<uuid>; text_vi/en, correct |
| EssayProblem / EssayHint | Đạt | essay:<uuid> / hint:<uuid>; prompt, assumptions, conclusion, solution / order, text |
| Attempt | Đạt | attempt:<uuid>; score 0–10, started_at, finished_at, status |
| AttemptAnswer | Đạt | answer:<uuid>; correct; các lựa chọn là relationship |
| Progress | Vũ | progress:<user uuid>:<grade>; user_id, level_id composite unique, completion, average_score, unlocked |
| ChatSession / ChatMessage | Đạt | chat:<uuid> / message:<uuid>; role, content, provider, created_at, feedback TODO |
| ImportLog | Sơn | import:<uuid>; admin_id, kind, success_count, error_count, created_at; constraint có, seed chưa cần |

Node được chọn khi có danh tính, nhiều liên kết, vòng đời hoặc cần truy vấn riêng. AttemptAnswer tách node để lưu nhiều đáp án và xem lại từng lần; EssayHint có thứ tự/mở dần; Progress là tổng hợp theo User×Level. Trạng thái học **từng Lesson** nằm trên `LEARNING`/`COMPLETED`, không nhầm Progress level với SRS Progress lesson. LevelProgress trong SRS được gộp thành node Progress. Metadata, vai trò, bản dịch, số đo đơn giản là properties; không tách mọi property thành node.

`GeometryConfig.config_json` chỉ cho payload renderer không cần traversal (Neo4j không lưu map như property); shape, bài, tiên quyết, lựa chọn và user history phải là graph. Khung hiện seed config dạng scalar. Note/version, saved drawing, quiz grouping/placement, essay self-review và consent token là TODO; chưa tự thêm schema chưa chốt vào runtime.

## Relationships và quyền ghi

| Relationship | Chủ ghi duy nhất | Ý nghĩa / cardinality dự kiến |
|---|---|---|
| Level-HAS_CHAPTER→Chapter | Sơn | 1→n, Chapter một Level |
| Chapter-HAS_TOPIC→Topic | Sơn | 1→n, Topic một Chapter |
| Topic-HAS_LESSON→Lesson | Sơn | 1→n, Lesson một Topic |
| Lesson/Topic-REQUIRES→Lesson/Topic | Sơn | n→n, dùng cùng loại endpoint, không chu trình, grade target ≤ source |
| Lesson-RELATED_TO→Lesson | Sơn | n→n, chiều source→target; nếu đối xứng phải MERGE cả hai chiều |
| Quadrilateral-IS_A→Quadrilateral | Sơn | từ loại cụ thể đến loại tổng quát; DAG, tránh vòng |
| Lesson-ABOUT→Quadrilateral | Sơn | n→n, cùng shape có bài ở nhiều lớp |
| Lesson-ILLUSTRATED_BY→GeometryConfig | Sơn | n→n |
| User-STUDIES_AT→Level | Vũ | đúng một cấp hiện tại; đổi cấp xóa cạnh cũ trong cùng transaction |
| User-COMPLETED/LEARNING→Lesson | Vũ | một cạnh mỗi cặp; timestamps, status; complete qua contract |
| User-HAS_PROGRESS→Progress-FOR_LEVEL→Level | Vũ | một Progress mỗi user/level; tổng hợp từ bài xuất bản và attempts |
| Topic-HAS_QUESTION→Question-HAS_OPTION→Option | Đạt | Question một Topic, Option một Question |
| Topic-HAS_ESSAY→EssayProblem-HAS_HINT→EssayHint | Đạt | Hint một Essay, order duy nhất trong Essay (service kiểm tra) |
| User-ATTEMPTED→Attempt-FOR_TOPIC→Topic | Đạt | Attempt một User/Topic trong demo, mỗi lần làm UUID mới |
| Attempt-HAS_ANSWER→AttemptAnswer-ANSWERS→Question | Đạt | một answer mỗi attempt/question |
| AttemptAnswer-SELECTED→Option | Đạt | 1/n theo loại câu hỏi; option phải thuộc question |
| User-HAS_CHAT→ChatSession-HAS_MESSAGE→ChatMessage | Đạt | mỗi message một session; thứ tự created_at + id |
| ChatSession-CONTEXT_LESSON→Lesson | Đạt | tham chiếu nội dung, không sửa Lesson |

ImportLog owner Sơn; quan hệ admin→log sẽ chốt khi import thực hiện. Đạt có thể tạo quan hệ xuất phát từ Topic/User do mình sở hữu theo bảng; không được sửa các node đó. Không hai domain ghi cùng cạnh. Vũ không sửa Attempt, Đạt không ghi Progress; Sơn không ghi COMPLETED.

## ID và an toàn dữ liệu

- Chuỗi ID có prefix loại, ASCII lower-case và không đổi khi sửa title. Level cố định; demo slug ổn định. User/Attempt/Answer/Chat dùng UUID mới khi tạo thật; không dùng email làm ID. IDs xuyên domain do DTO truyền, không suy ra từ tên hiển thị.
- MERGE node theo `id` dưới unique constraint, SET metadata riêng; MATCH endpoint tồn tại trước MERGE cạnh. Không MERGE cả pattern dài có node chưa match; không tạo user/topic hộ domain khác.
- Repository dùng `$parameters` cho input, không f-string Cypher người dùng. Grade 6–9, role/status allowlist và tồn tại endpoint được service kiểm tra.
- Cardinality/kiến thức thấp hơn/acyclic/đáp án đúng không được unique constraint kiểm hết. Import validate batch trước; transaction ghi atomic, kiểm tra `EXISTS { MATCH (target)-[:REQUIRES*1..]->(source) }` để chặn vòng. Đồng thời hóa ghi cần review khi triển khai.
- Published nội dung mới tính mẫu số hoàn thành. Progress là projection có thể tính lại, không nguồn điểm. Chưa chốt trung bình latest/all attempts: OPEN_QUESTIONS.md.
- Seed chạy lại an toàn, **ghi đè giá trị demo cố định**, không migration dữ liệu thật. Tất cả node seed có `demo=true`; không nhập bài thật vào node demo. Seed tạo 4 level, 4 chapter, 5 topic/lesson, taxonomy 8 shape, một attempt/answer, essay/hint và chat mock.
- Taxonomy cố ý chưa nối bình hành→hình thang vì định nghĩa bao hàm hình thang chưa được SGK xác nhận. Hình chữ nhật→nội tiếp là tính chất đúng; hình vuông có hai đường IS_A riêng, không diễn giải mọi hình thoi là chữ nhật.

## Truy vấn graph có thể chạy

Xem `database/examples.cypher`; chạy `python -m scripts.db queries` hoặc paste từng câu vào Neo4j Browser. Có tiên quyết 8 bước, taxonomy 5 bước, bài cùng loại hình, ôn tiên quyết từ điểm thấp, ngữ cảnh AI 3 bước và tiếp tục bài dở. Bounds là giới hạn demo, không tuyên bố traversal đầy đủ mọi graph. Query ôn tập trả rỗng với seed điểm 10 là đúng.

```cypher
MATCH (:Lesson {id:'lesson:9:cyclic'})-[:REQUIRES*1..8]->(p:Lesson)
RETURN DISTINCT p.id, p.title_vi;

MATCH (:Quadrilateral {id:'shape:square'})-[:IS_A*1..5]->(q)
RETURN DISTINCT q.name_vi;

MATCH (:Lesson {id:'lesson:8:rectangle'})-[:REQUIRES|RELATED_TO*0..3]->(l:Lesson)
WHERE l.status='published'
RETURN DISTINCT l.id, l.content_vi LIMIT 8;
```

Các đường đi biến độ dài tận dụng graph để tìm nền tảng nhiều cấp và taxonomy đa cha; không chỉ CRUD như bảng SQL. AI context là truy vấn nguồn nội dung có kiểm soát, chưa là RAG production. Admin cần bảo vệ việc đọc properties đáp án trong workflow thật.

## Mở rộng domain Vũ sau skeleton

AuthSession (id/hash unique, last_seen, auth_version) và AuthToken (id/hash unique, kind, expires_at, used_at) do Vũ ghi, User-HAS_AUTH_SESSION/HAS_AUTH_TOKEN trỏ đến các node này. User thêm password_hash Argon2id, starting_grade, email_verified, guardian_required/consent/email, status, auth_version, failed_logins/locked_until, activation_channel. AuthToken/session không có raw token/password. Counter auth_lock/progress_lock chỉ để lấy write lock, không là thống kê học tập. Dữ liệu tài khoản local mới không có demo=true nên reset demo không xóa chúng. Ownership các node/cạnh cũ giữ nguyên.

## Node do Đạt bổ sung sau merge

- `EssayReview`: id unique, rating, hints_used, answer_text, created_at. `(User)-[:REVIEWED_ESSAY]->(EssayReview)-[:FOR_ESSAY]->(EssayProblem)`; Đạt sở hữu ghi, mỗi lần review node mới.
- `AIQuotaDay`: id unique theo `ai-quota:{user_id}:{YYYY-MM-DD}`, user_id/day/used/pending/lock. Chủ sở hữu Đạt; property user_id phục vụ lookup quota, không ghi property của User. Ngày UTC+7 theo implementation hiện tại.

Hai constraints nay nằm trong constraints.cypher; runtime lazy IF NOT EXISTS còn giữ để tương thích database đã setup. Không thay schema User/Progress của Vũ. Xóa toàn bộ dữ liệu cá nhân cần cleanup thêm hai loại node này qua owner contract.
