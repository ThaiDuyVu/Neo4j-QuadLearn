# Vũ – identity_learning_path

## 1. Owner và mục tiêu

Vũ sở hữu `app/features/identity_learning_path/`. Identity & Learning Path: danh tính, cấp độ và projection tiến độ. Đã phát triển nghiệp vụ local trên branch Vũ: AUTH cơ bản, hồ sơ, cấp độ/progress, review và admin user management. Email/OAuth/xóa dữ liệu/thống kê liên domain còn TODO. Xem [bản giải thích code](../../../docs/VU_NGHIEP_VU_VA_GIAI_THICH_CODE.md) để hiểu luồng và trạng thái từng FR. Bảng trạng thái trong tài liệu giải thích cập nhật nghiệm thu local, không chứng nhận toàn bộ SRS.

## 2. FR liên quan và ưu tiên SRS

| FR-ID | Công việc nghiệp vụ | Ưu tiên | Đối chiếu triển khai |
|---|---|---|---|
| FR-AUTH-01 | Đăng ký bằng email + mật khẩu (họ tên, email, mật khẩu, lớp 6/7/8/9) | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-02 | Mật khẩu tối thiểu 8 ký tự, gồm chữ và số; email không trùng | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-03 | Gửi email xác thực; chỉ tài khoản đã xác thực mới lưu tiến độ | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-04 | Đăng nhập bằng email + mật khẩu | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-05 | Đăng nhập bằng Google (OAuth 2.0); liên kết nếu email đã tồn tại | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-06 | Quên mật khẩu: gửi liên kết đặt lại, hết hạn sau 30 phút, dùng một lần | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-07 | Đổi mật khẩu khi đã đăng nhập (yêu cầu mật khẩu cũ) | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-08 | Đăng xuất; phiên hết hạn sau 7 ngày không hoạt động | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-09 | Chỉnh sửa hồ sơ (tên, lớp, ảnh đại diện, ngôn ngữ) | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-10 | Khóa tạm thời tài khoản sau 5 lần đăng nhập sai liên tiếp (15 phút) | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-11 | Xóa tài khoản và dữ liệu cá nhân theo yêu cầu | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AUTH-12 | Với HS dưới 16 tuổi, yêu cầu email phụ huynh/người giám hộ xác nhận đồng ý trước khi kích hoạt tài khoản | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LRN-05 | Đánh dấu "đã học xong" từng bài; điều hướng bài trước/sau | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-01 | Trang tổng quan: % hoàn thành theo cấp độ, chương và chủ đề | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-02 | Lịch sử làm bài: ngày giờ, bài, điểm, thời gian; xem lại bài và đáp án đã chọn | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-03 | Biểu đồ điểm theo thời gian | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-04 | Thống kê điểm mạnh/yếu theo chủ đề | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-05 | Tiếp tục học: quay lại đúng bài đang học dở | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-PG-06 | Gợi ý chủ đề nên ôn lại (dựa trên quy tắc đơn giản, ví dụ điểm < 5) | C | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AD-01 | Đăng nhập quản trị với vai trò riêng, bảo vệ nâng cao | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AD-09 | Quản lý người dùng: tìm kiếm, khóa/mở khóa tài khoản | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AD-10 | Thống kê: số HS, lượt học, bài làm nhiều/ít, câu hỏi AI thường gặp, đánh giá chatbot | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-AD-11 | Cấu hình hệ thống: hạn mức hỏi AI, thời gian phiên | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-I18-01 | Chuyển đổi Việt/Anh ở mọi màn hình; ghi nhớ lựa chọn theo tài khoản | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-01 | Khi đăng ký, HS chọn lớp (6, 7, 8, 9); lớp này là cấp độ khởi đầu | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-02 | HS đổi cấp độ trong hồ sơ; tiến độ của từng cấp độ được lưu riêng | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-03 | Lộ trình hiển thị theo cấp độ; mỗi chủ đề/bài/câu hỏi gắn nhãn lớp và mức nhận thức | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-05 | HS truy cập tự do nội dung cấp thấp hơn để ôn tập | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-06 | Mở khóa cấp cao hơn khi hoàn thành ≥ 70% bài học và điểm trung bình ≥ 6/10 (ngưỡng cấu hình được); HS có thể chọn "học vượt" kèm cảnh báo | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-07 | Mỗi bài hiển thị kiến thức tiên quyết (liên kết về bài nền ở cấp dưới) | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-08 | Khi điểm một chủ đề < 5/10, gợi ý ôn các bài tiên quyết ở cấp thấp hơn | S | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-10 | Dashboard hiển thị tiến độ riêng cho từng cấp độ | M | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |
| FR-LV-11 | Bài kiểm tra xếp loại đầu vào để gợi ý cấp độ phù hợp | C | Xem trạng thái chi tiết ở tài liệu giải thích, mục 2 |

M = Must, S = Should, C = Could của sản phẩm; skeleton hoãn cả các Must phức tạp. Ánh xạ toàn bộ: `docs/SRS_TRACEABILITY.md`; stories/acceptance: `docs/PRODUCT_BACKLOG.md`. Giữ đúng business rules ở hai tài liệu này, không suy ra từ mock.

## 3. Màn hình

SCR-02/03/04/11/12/16/17; SCR-13 dashboard tổng hợp. Hiện có overview/account/path/profile/admin, khai báo tại registry.py; không phải toàn bộ UI SRS đã được nghiệm thu.

## 4. Graph ownership và queries

User, Progress; STUDIES_AT, LEARNING, COMPLETED, HAS_PROGRESS, FOR_LEVEL. Xem `docs/GRAPH_SCHEMA.md` cho endpoint/cardinality và ID. Queries cần làm: User theo ID/email; level hiện tại; published lesson counts và COMPLETED; bài LEARNING gần nhất; Progress theo user/level; prerequisites thông qua ContentReader, không query nội bộ Sơn.

Không ghi node/cạnh owner khác. Các cạnh tham chiếu User/Topic chỉ được ghi theo bảng ownership. Query tham số `$id/$grade`, MATCH endpoint tồn tại trước MERGE; constraint không tự validate business.

## 5. Services và file bắt đầu

IdentityService quản lý session/profile/admin; AuthService đăng ký/login/token/password; LearningPathService progress/access/review; IdentityRepository và ProgressRepository chứa Cypher. Profile/level được tổ chức trong các service này, không thêm abstraction thừa.

Mở các file: `registry.py; pages/overview.py; services/identity.py; repositories/identity.py; tests/test_identity.py` (tương đối trong folder này). Thêm page/service/repository/model/test trong thư mục tương ứng; thêm PageSpec ở `registry.py`. Không phải sửa `app/main.py`. Tests/fakes đọc ports chung; không dùng query database thật trong unit.

## 6. Input/output contracts và dependencies

Cung cấp IdentityReader → CurrentUser|None. Nhận ContentReader → LessonSummary[] và AssessmentReader → AttemptSummary[]. ProgressWriter đã có implementation trong LearningPathService, được inject vào ctx.progress; write đòi session đã kích hoạt, demo bị chặn.

DTO ở `app/shared/models/dto.py`, ports ở `app/shared/contracts/ports.py`. Empty list/None có nghĩa không có dữ liệu; lỗi kết nối không được đổi thành dữ liệu giả. `core/bootstrap.py` nối implementation. Không import repository/service domain khác; readers truyền qua AppContext. Shared API mới phải cả nhóm review và có test consumer/provider trước merge.

## 7. Thứ tự triển khai và checklist

Đọc SRS mapping → chốt câu hỏi domain → bổ sung model/repository → test service qua fake ports → thêm page/registry → chạy test domain → demo Neo4j → PR. Làm Must trước Should/Could; chia PR nhỏ theo chức năng, không đánh dấu checklist chỉ vì có placeholder.

### Must

- [x] Tạo repository tìm User theo ID và email với unique email constraint.
- [x] Thêm validate mật khẩu chữ/số, lớp 6–9 và hash; không lưu plaintext.
- [x] Thiết kế email verification và guardian consent trước khi kích hoạt tài khoản (chưa kết nối email).
- [x] Thêm session current_user và kiểm tra role ở service, thay user demo cố định.
- [x] Thêm ProgressWriter.complete_lesson idempotent và kiểm tra verified/consent.
- [x] Tạo query tổng hợp published lessons/COMPLETED theo mỗi Level.
- [x] Hiển thị dashboard/tiếp tục bài dở với ContentReader và lịch sử AssessmentReader.
- [x] Viết test trường hợp không user, chưa verified, grade sai và projection không đếm draft.

### Should

- [x] Viết service unlock threshold cấu hình; xử lý thiếu điểm và boundary 70%/6 điểm.
- [x] Thêm cảnh báo/xác nhận học vượt; không khóa cấp dưới.
- [x] Hiển thị điểm yếu và gợi ý REQUIRES từ ContentReader.
- [x] Khóa login sai 5 lần/15 phút và sửa hồ sơ local.
- [ ] Contract xóa dữ liệu với Đạt và xóa tài khoản đầy đủ.
- [x] Tìm người dùng và lock/unlock bằng admin service.
- [ ] Dashboard aggregate chat/AI/toàn hệ thống và bảo vệ admin nâng cao.

### Could

- [ ] Chốt contract bài xếp loại với Đạt; tính gợi ý lớp theo kết quả.
- [x] Gợi ý ôn chủ đề từ điểm thấp, có nguồn dữ liệu và test.

## 8. Tiêu chí hoàn thành

AUTH: validation/hash/role/session/verify/consent được test, không còn danh tính demo ở flow thật. Progress: phần trăm đúng chỉ published, mỗi lớp riêng, resume đúng bài, không ghi Attempt. Unlock: boundary/cấu hình/học vượt/lớp dưới có test và Q4 đã chốt. Không gọi AUTH done khi OAuth/email bắt buộc còn TODO.

Mỗi nhóm chức năng cần PR review, tests happy/error/boundary và demo đúng tiêu chí FR/PB liên quan. Ghi TODO phần chưa làm. DoD staging/70% coverage/UAT của SRS là mục tiêu sản phẩm, chưa được skeleton chứng nhận; đừng ghi “PASS SRS” chỉ vì unit tests nền pass.

## 9. Test riêng

```text
python -m pytest app/features/identity_learning_path/tests -q
python -m pytest tests/test_boundaries.py tests/test_navigation.py -q
```

Test domain không cần Neo4j. Khi DB demo sẵn, bật `QUADLEARN_INTEGRATION=1` và chạy integration theo docs/RUN_PROJECT.md. Smoke pages dùng fake contracts; kiểm UI thật thêm qua sidebar. Test không phải full FR acceptance.

## 10. Demo

Mở Tài khoản để đăng ký/kích hoạt token local/login, rồi Dashboard/Lộ trình/Hồ sơ/Admin. Chọn demo chỉ đọc để xem fixture. Không gọi token local là email thật. Hướng dẫn demo chung: `docs/DEMO_GUIDE.md`. Nếu DB chưa chạy, page báo lỗi hướng dẫn; không báo kết nối PASS giả.

## 11. Giới hạn sửa file

Được sửa folder mình và các file mới trong đó. Không sửa folder hai bạn khác, không trực tiếp query/ghi nội bộ họ. `app/core`, `app/shared`, `database`, `.env.example`, `compose.yaml`, dependencies và docs kiến trúc là vùng chung: thông báo cả nhóm, giải thích tương thích, review trước merge. File `.env` local không commit. Registry path không trùng; không hardcode secret/data HS thật. Git cá nhân: GIT_WORKFLOW.md.
