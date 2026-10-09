# Bộ dữ liệu demo QuadLearn — quadlearn-demo-v1

## 1. Nội dung và mục đích

Bổ sung **16 bài học**, **32 câu trắc nghiệm single-choice**, **4 bài tự luận với 3 gợi ý/đề**, cùng quan hệ tiên quyết và liên kết loại hình. Mỗi lớp 6–9 có 4 bài, 8 câu hỏi và 1 tự luận. Bộ graph nền còn chứa phân loại tứ giác và cấu hình minh họa.

Dữ liệu nhằm trình bày hành trình học và đặc điểm Neo4j; không cam kết bao phủ SGK, mọi FR hoặc toàn bộ chương trình. Nội dung tiếng Việt có định nghĩa, tính chất, công thức, câu tự kiểm tra. `title_en` có tên tiếng Anh; nội dung tiếng Anh vẫn là placeholder có ghi TODO, chưa dịch đầy đủ.

- `database/demo/content.json`: nguồn học liệu, đáp án và tiên quyết; sửa tại đây khi bổ sung dữ liệu demo.
- `scripts/demo_data.py`: kiểm tra dữ liệu, import Cypher có parameter, tạo tài khoản và trạng thái qua service nghiệp vụ hiện tại.
- `tests/test_demo_data.py`: kiểm tra liên kết, chu trình, đáp án và ID trước khi ghi.
- `docs/DEMO_GUIDE.md`: thứ tự thao tác và lời trình bày theo bộ này.

## 2. Tài khoản thử nghiệm

Mật khẩu mặc định: **`Demo123456789`**, công khai chỉ cho fixture local. Password được băm Argon2 khi lưu DB. `QUADLEARN_DEMO_PASSWORD` là biến tùy chọn để đặt mật khẩu khác khi tạo mới hoặc reset; chạy lại thông thường không đổi mật khẩu tài khoản đã có. Mật khẩu Neo4j luôn lấy từ `.env`, không dùng credential này cho database.

| Email | Lớp / vai trò | Hoàn thành | Điểm TB | Mục đích |
|---|---|---:|---:|---|
| demo.start@quadlearn.local | 8 / student | 0% | Chưa có | Học từ đầu, kiểm tra tính giờ |
| demo.path@quadlearn.local | 8 / student | 50% | 10 | Học dở hình thoi, flow chính |
| demo.ready@quadlearn.local | 8 / student | 75% | 10 | Đủ ngưỡng lên lớp 9, chưa đổi lớp |
| demo.review@quadlearn.local | 8 / student | 0% | 0 | Ôn kiến thức nền của chủ đề yếu |
| demo.junior@quadlearn.local | 6 / student | 25% | 10 | Học trực quan lớp 6 |
| demo.senior@quadlearn.local | 9 / student | 25% | 10 | Tứ giác nội tiếp lớp 9 |
| demo.manager@quadlearn.local | 8 / admin | 0% | Chưa có | Quản lý người dùng |

Các tài khoản có `demo=false` để được ghi dữ liệu, `fixture_pack=quadlearn-demo-v1` để script nhận diện khi reset. Tất cả là người học thử nghiệm 18 tuổi, đã kích hoạt local; không giả lập xác minh phụ huynh. ID ổn định dạng `user:fixture:path`. Không có session đăng nhập còn lại sau khi script khởi tạo.

Lịch sử điểm là **fixture được script nộp qua service chấm bài**, không phải kết quả người thật đã học. Path/ready làm đúng hai câu chủ đề hình chữ nhật; review chọn sai cả hai câu. Junior làm đúng chủ đề chữ nhật lớp 6; senior làm đúng chủ đề nội tiếp. Start/manager không có bài làm sẵn.

Tài khoản admin cũ `admin@quadlearn.local`, tài khoản demo chỉ đọc cũ và các tài khoản khác được giữ nguyên. Fixture manager cung cấp admin có thể tạo lại trên máy khác mà không sửa tài khoản admin cũ.

## 3. Danh sách bài và đáp án phục vụ demo

### Lớp 6

| Bài | ID | Tiên quyết trực tiếp |
|---|---|---|
| Nhận biết tứ giác | `lesson:6:quadrilateral` |  |
| Hình chữ nhật trực quan | `lesson:6:rectangle` | `lesson:6:quadrilateral` |
| Hình vuông và diện tích | `lesson:6:square` | `lesson:6:rectangle` |
| Chu vi và đơn vị đo | `lesson:6:perimeter` | `lesson:6:quadrilateral` |

| Chủ đề | Câu hỏi | Đáp án đúng |
|---|---|---|
| `topic:6:quadrilateral` | Tứ giác có bao nhiêu cạnh? | **4** |
| `topic:6:quadrilateral` | Tứ giác ABCD có các đỉnh nào? | **A, B, C, D** |
| `topic:6:rectangle` | Hình chữ nhật dài 4 cm, rộng 3 cm có diện tích bao nhiêu? | **12 cm²** |
| `topic:6:rectangle` | Chu vi của hình chữ nhật dài 4 cm, rộng 3 cm là bao nhiêu? | **14 cm** |
| `topic:6:square` | Hình vuông cạnh 5 cm có diện tích bao nhiêu? | **25 cm²** |
| `topic:6:square` | Hình vuông cạnh 5 cm có chu vi bao nhiêu? | **20 cm** |
| `topic:6:perimeter` | Đơn vị nào dùng để đo diện tích? | **cm²** |
| `topic:6:perimeter` | Tứ giác có các cạnh 2, 3, 4, 5 cm có chu vi bao nhiêu? | **14 cm** |

**Tự luận:** Một sân hình vuông có cạnh 5 m. Tính diện tích và chu vi.

**Lời giải:** S = 5² = 25 m²; P = 4 × 5 = 20 m.

### Lớp 7

| Bài | ID | Tiên quyết trực tiếp |
|---|---|---|
| Hai đường thẳng song song | `lesson:7:parallel` | `lesson:6:rectangle` |
| Góc kề bù và góc đối đỉnh | `lesson:7:angles` | `lesson:6:quadrilateral` |
| Vuông góc và chiều cao | `lesson:7:perpendicular` | `lesson:7:angles` |
| Trung điểm của đoạn thẳng | `lesson:7:midpoint` | `lesson:6:perimeter` |

| Chủ đề | Câu hỏi | Đáp án đúng |
|---|---|---|
| `topic:7:parallel` | Hai đường thẳng phân biệt song song có bao nhiêu điểm chung? | **0** |
| `topic:7:parallel` | Khi một đường cắt hai đường song song, hai góc so le trong như thế nào? | **Bằng nhau** |
| `topic:7:angles` | Một góc của cặp kề bù bằng 65°. Góc còn lại bằng bao nhiêu? | **115°** |
| `topic:7:angles` | Hai góc đối đỉnh có tính chất nào? | **Bằng nhau** |
| `topic:7:perpendicular` | Hai đường vuông góc tạo góc bao nhiêu độ? | **90°** |
| `topic:7:perpendicular` | Chiều cao dùng trong công thức diện tích cần như thế nào với đáy? | **Vuông góc** |
| `topic:7:midpoint` | M là trung điểm AB và AB = 10 cm. AM bằng bao nhiêu? | **5 cm** |
| `topic:7:midpoint` | Điều kiện nào đủ để M là trung điểm AB? | **M thuộc đoạn AB và MA = MB** |

**Tự luận:** Hai góc kề bù, một góc bằng 65°. Tính góc còn lại.

**Lời giải:** Hai góc kề bù có tổng 180°. Góc còn lại = 180° − 65° = 115°.

### Lớp 8

| Bài | ID | Tiên quyết trực tiếp |
|---|---|---|
| Hình bình hành | `lesson:8:parallelogram` | `lesson:7:parallel`, `lesson:7:midpoint` |
| Hình chữ nhật và tính chất | `lesson:8:rectangle` | `lesson:8:parallelogram` |
| Hình thoi và đường chéo | `lesson:8:rhombus` | `lesson:8:parallelogram`, `lesson:7:perpendicular` |
| Hình vuông: liên hệ chữ nhật và thoi | `lesson:8:square` | `lesson:8:rectangle`, `lesson:8:rhombus` |

| Chủ đề | Câu hỏi | Đáp án đúng |
|---|---|---|
| `topic:8:parallelogram` | Hình bình hành có đáy 6 cm, chiều cao 4 cm. Diện tích bằng bao nhiêu? | **24 cm²** |
| `topic:8:parallelogram` | Hai đường chéo hình bình hành có tính chất nào? | **Cắt nhau tại trung điểm mỗi đường** |
| `topic:8:rectangle` | Hình chữ nhật có bao nhiêu góc vuông? | **4** |
| `topic:8:rectangle` | Hai đường chéo hình chữ nhật có tính chất nào? | **Bằng nhau và cắt nhau tại trung điểm** |
| `topic:8:rhombus` | Hình thoi có đường chéo 6 cm và 4 cm. Diện tích bằng bao nhiêu? | **12 cm²** |
| `topic:8:rhombus` | Hai đường chéo hình thoi luôn có tính chất nào? | **Vuông góc** |
| `topic:8:square` | Hình vuông thuộc những loại nào? | **Cả hình chữ nhật và hình thoi** |
| `topic:8:square` | Hình chữ nhật có thêm điều kiện nào thì là hình vuông? | **Hai cạnh kề bằng nhau** |

**Tự luận:** Tính diện tích hình chữ nhật có chiều dài 4 cm, chiều rộng 3 cm.

**Lời giải:** S = a × b = 4 × 3 = 12 cm².

### Lớp 9

| Bài | ID | Tiên quyết trực tiếp |
|---|---|---|
| Tứ giác nội tiếp | `lesson:9:cyclic` | `lesson:8:rectangle` |
| Tính góc trong tứ giác nội tiếp | `lesson:9:opposite-angles` | `lesson:9:cyclic`, `lesson:7:angles` |
| Nhận biết tứ giác nội tiếp | `lesson:9:cyclic-test` | `lesson:9:cyclic`, `lesson:9:opposite-angles` |
| Ôn tập quan hệ các loại tứ giác | `lesson:9:review` | `lesson:9:cyclic-test`, `lesson:8:square` |

| Chủ đề | Câu hỏi | Đáp án đúng |
|---|---|---|
| `topic:9:cyclic` | Tứ giác nội tiếp có góc A = 70°. Góc đối C bằng bao nhiêu? | **110°** |
| `topic:9:cyclic` | Một tứ giác nội tiếp có bao nhiêu đỉnh nằm trên cùng đường tròn? | **4** |
| `topic:9:opposite-angles` | ABCD nội tiếp, B = 100°. D bằng bao nhiêu? | **80°** |
| `topic:9:opposite-angles` | Cặp nào là góc đối trong tứ giác ABCD? | **A và C** |
| `topic:9:cyclic-test` | Tứ giác lồi ABCD có A = 80°, C = 100°. Kết luận nào đúng? | **ABCD nội tiếp** |
| `topic:9:cyclic-test` | Điều kiện góc nào nhận biết tứ giác lồi nội tiếp? | **Hai góc đối bù nhau** |
| `topic:9:review` | Loại hình nào luôn là tứ giác nội tiếp? | **Hình chữ nhật** |
| `topic:9:review` | Một hình thoi nội tiếp phải là hình gì? | **Hình vuông** |

**Tự luận:** Tứ giác lồi ABCD nội tiếp có góc A = 70°, góc B = 100°. Tính góc C và D.

**Lời giải:** A + C = 180° nên C = 110°. B + D = 180° nên D = 80°.

## 4. Chạy lại và reset

Tạo lần đầu trên máy đã setup:

```bash
python -m scripts.db init
python -m scripts.demo_data
```

Sau đó chỉ cần `python -m scripts.demo_data` nếu muốn cập nhật bộ học liệu. Script dùng ID ổn định và MERGE; chạy lại không nhân đôi node/quan hệ hay tạo thêm bài làm cho tài khoản đã khởi tạo. Bộ nội dung fixture được cập nhật theo JSON, gồm năm bài học, một câu hỏi và một đề tự luận dùng lại từ seed gốc; nội dung tự tạo có ID ngoài bộ này không bị sửa. Nếu ID trong bộ trùng dữ liệu không mang `demo=true`, script dừng thay vì ghi đè.

**Reset có chủ ý trước buổi demo:**

```bash
python -m scripts.demo_data --reset-demo-users --yes
```

Lệnh này **xóa bảy tài khoản fixture và toàn bộ lịch sử riêng của chúng**, gồm session/token, tiến độ, attempt/answer, chat/message, self-review và quota; sau đó tạo lại trạng thái bảng trên. Cần đăng nhập lại trên giao diện. Không xóa học liệu, taxonomy, Docker volume, tài khoản admin cũ hoặc dữ liệu của người dùng khác. Chỉ chạy khi `APP_ENV=development`; thiếu `--yes` thì bị từ chối.

Không dùng `python -m scripts.db reset --yes` hoặc `docker compose down -v` để làm lại flow này: chúng có phạm vi xóa khác/lớn hơn. Khi đã thêm dữ liệu riêng vào fixture thì reset sẽ làm mất dữ liệu riêng đó.

Nếu đặt mật khẩu riêng, trước khi tạo/reset:

macOS: `export QUADLEARN_DEMO_PASSWORD='mat-khau-thu-nghiem-co-chu-va-so'`.

PowerShell: `$env:QUADLEARN_DEMO_PASSWORD = 'mat-khau-thu-nghiem-co-chu-va-so'`.

Mật khẩu phải có chữ và số, 8–256 ký tự. Thay giá trị minh họa bằng mật khẩu đáp ứng điều kiện. Đừng dùng mật khẩu cá nhân/production. Không cần commit `.env`.

## 5. Kiểm tra nhanh

```bash
python -m scripts.db check
python -m pytest -q tests/test_demo_data.py
```

Trong Neo4j Browser:

```cypher
MATCH (l:Level)-[:HAS_CHAPTER]->(:Chapter)-[:HAS_TOPIC]->(:Topic)-[:HAS_LESSON]->(lesson:Lesson)
WHERE lesson.demo_pack='quadlearn-demo-v1'
RETURN l.grade AS lop,count(DISTINCT lesson) AS so_bai ORDER BY lop;
```

Kỳ vọng bốn dòng, mỗi lớp 4 bài. Với database có thêm nội dung của thành viên, số bài trên giao diện có thể nhiều hơn 4; khi đó tỷ lệ hoàn thành và ngưỡng mở cấp sẽ thay đổi. Không xóa nội dung thành viên để ép kết quả; dùng database demo riêng hoặc điều chỉnh flow theo tổng bài thực tế.

Kiểm tra tài khoản, không trả password hash:

```cypher
MATCH (u:User {fixture_pack:'quadlearn-demo-v1'})-[:STUDIES_AT]->(l:Level)
RETURN u.email AS email,u.role AS vai_tro,u.status AS trang_thai,l.grade AS lop
ORDER BY email;
```

Lỗi driver có warning thuộc tính mới chưa xuất hiện trên lần chạy đầu thường không phải lỗi import; kiểm tra exit code và kết quả. Nếu tạo thất bại giữa chừng, xem lỗi trước khi reset riêng fixture, không xóa database toàn bộ.

## 6. Kết quả kiểm chứng ngày 09/10/2026

- **PASS: 191 tests**, gồm 179 unit/UI và 12 integration Neo4j (bật `QUADLEARN_INTEGRATION=1`).
- **PASS:** cả bảy tài khoản đăng nhập được; vai trò và tiến độ ban đầu đúng bảng; mỗi cấp đọc được 4 bài, 8 câu hỏi, 1 tự luận.
- **PASS:** luồng service trên DB thật: 50% đang khóa lớp 9 → nộp quiz → học xong hình thoi → 75% → chuyển lớp 9 → lưu quiz, tự luận và chat.
- **PASS:** năm trang Streamlit render với DB thật bằng AppTest; sửa lỗi nhãn đáp án lấy nhầm dữ liệu của câu cuối khi có nhiều câu trên trang.
- **PASS:** chạy lại không tăng node/relationship; reset fixture phục hồi trạng thái; các node User ngoài fixture, gồm admin cũ, được giữ nguyên.
- Các fixture đã được trả về trạng thái ban đầu sau kiểm tra, sẵn sàng demo.
- **CHƯA KIỂM CHỨNG:** toàn bộ thao tác bằng trình duyệt thủ công và chạy trên Windows trong lần này. Các lệnh dùng Python/Docker Compose chung hai OS.

Driver hiện có cảnh báo deprecation khi chạy với Python 3.14; các kiểm tra trên vẫn pass. Không coi cảnh báo đó là đã nghiệm thu đầy đủ SRS.
