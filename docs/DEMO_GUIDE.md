# QuadLearn — Flow demo với dữ liệu đầy đủ để trình bày

Hướng dẫn cho bộ **quadlearn-demo-v1**, cập nhật ngày **09/10/2026**. Flow chính 15–20 phút; bản rút gọn 5–7 phút ở cuối tài liệu. Học liệu là bộ minh họa phục vụ bài tập Neo4j, chưa phải giáo trình đầy đủ lớp 6–9.

**Đã tạo dữ liệu trên Neo4j local hiện tại.** Mở ứng dụng tại <http://localhost:8501>; Neo4j Browser tại <http://localhost:7474>. Danh sách bài, đáp án, trạng thái tài khoản và cơ chế tạo lại ở [DEMO_DATA.md](DEMO_DATA.md).

## 1. Chuẩn bị và chọn tài khoản

### 1.1. Khởi động / tạo dữ liệu trên máy khác

Nếu máy đã setup và có graph nền:

**macOS Terminal:**

```bash
source .venv/bin/activate
docker compose up -d --wait
python -m scripts.db check
python -m scripts.demo_data
python -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
docker compose up -d --wait
python -m scripts.db check
python -m scripts.demo_data
python -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501
```

Máy mới cần tạo `.env`, cài dependencies theo [Windows](SETUP_WINDOWS.md) hoặc [macOS](SETUP_MACOS.md). Chạy `python -m scripts.db init` **trước** `python -m scripts.demo_data` để tạo graph nền lần đầu. Nếu chạy `db init` lại sau đó, chạy tiếp `demo_data` để khôi phục nội dung demo mở rộng.

`demo_data` cập nhật bộ học liệu demo theo ID; tài khoản đã có thì giữ nguyên lịch sử và trạng thái. Không tự reset mỗi lần chạy ứng dụng.

### 1.2. Tài khoản đã chuẩn bị

Mật khẩu mặc định công khai của **bảy tài khoản thử nghiệm** dưới đây: **`Demo123456789`**. Đây là credential demo dùng local; không phải mật khẩu Neo4j. Nếu người setup dùng `QUADLEARN_DEMO_PASSWORD`, sử dụng mật khẩu họ đã đặt.

| Email | Vai trò / cấp | Trạng thái ban đầu | Dùng ở đâu |
|---|---|---|---|
| `demo.path@quadlearn.local` | student / lớp 8 | 2/4 bài = 50%, điểm TB 10; đang học Hình thoi | **Flow chính**: thêm một bài → 75% → lớp 9 |
| `demo.start@quadlearn.local` | student / lớp 8 | 0%, chưa có điểm | Demo học từ đầu hoặc làm bài tính giờ |
| `demo.ready@quadlearn.local` | student / lớp 8 | 3/4 bài = 75%, điểm TB 10 | Chuyển cấp ngay nếu thời gian ngắn |
| `demo.review@quadlearn.local` | student / lớp 8 | 0%, điểm TB 0 | Gợi ý ôn tập theo chủ đề yếu |
| `demo.junior@quadlearn.local` | student / lớp 6 | 1/4 bài = 25%, điểm TB 10 | Minh họa nội dung trực quan lớp 6 |
| `demo.senior@quadlearn.local` | student / lớp 9 | 1/4 bài = 25%, điểm TB 10 | Góc đối và bài tập tứ giác nội tiếp |
| `demo.manager@quadlearn.local` | admin / lớp 8 | Tài khoản quản trị thử nghiệm | Tìm, khóa và mở khóa tài khoản |

Các tài khoản này đã kích hoạt, có mật khẩu băm và được đăng nhập/ghi dữ liệu. Chúng **khác tài khoản `student@example.invalid` chỉ đọc**. Tài khoản admin cũ `admin@quadlearn.local` và mật khẩu của nó vẫn giữ nguyên.

### 1.3. Checklist trước buổi trình bày

- [ ] Neo4j chạy; `python -m scripts.db check` báo kết nối OK.
- [ ] Đăng nhập thử tài khoản `demo.path`, xem 50%, điểm 10, bài tiếp tục Hình thoi.
- [ ] Lớp 8 có đúng bốn bài demo: Hình bình hành, Hình chữ nhật, Hình thoi, Hình vuông.
- [ ] Chủ đề `topic:8:rectangle` có hai câu hỏi.
- [ ] Không có bài kiểm tra tính giờ đang làm; còn lượt hỏi trợ lý.
- [ ] Mở sẵn Neo4j Browser bằng credentials `.env`, không chiếu mật khẩu lên màn hình.

**Trạng thái bảng trên là sau lần tạo đầu hoặc reset có chủ ý.** Các thao tác trong buổi demo lưu thật và làm thay đổi trạng thái. Nếu đã chạy thử, xem [cách reset riêng fixture](DEMO_DATA.md#4-chạy-lại-và-reset) để phục hồi trước buổi trình bày. Reset xóa lịch sử của bảy tài khoản demo này, không xóa tài khoản người dùng khác hoặc học liệu.

## 2. Flow chính: một người học từ lớp 8 lên lớp 9

| Bước | Màn hình | Thời gian | Chứng minh điều gì |
|---|---|---:|---|
| 1 | Trang chủ → Tài khoản | 1 phút | Danh tính người học |
| 2 | Tiến độ → Lộ trình | 2 phút | Tiến độ 50%, tiếp tục Hình thoi, tiên quyết |
| 3 | Nội dung & Hình học | 2 phút | Lý thuyết, mô phỏng, công thức |
| 4 | Bài tập và trợ lý học tập | 2 phút | Chấm hai câu và lưu lịch sử |
| 5 | Lộ trình → Hồ sơ | 3 phút | Hoàn thành thêm một bài, đạt 75%, chuyển cấp |
| 6 | Bài tập lớp 9 | 2 phút | Nội dung và bài tập đổi theo cấp hiện tại |
| 7 | Tự luận và trợ lý | 2 phút | Gợi ý ba bước, tự đánh giá, ngữ cảnh graph |
| 8 | Neo4j Browser | 3 phút | Phân loại hình, tiên quyết, dữ liệu đã lưu |
| 9 | Tài khoản cần ôn / admin | 2 phút | Các tình huống mở rộng tùy thời gian |

### Bước 1 — Giới thiệu và đăng nhập

Mở **Trang chủ**, giới thiệu mục tiêu học tứ giác lớp 6–9. Vào **Tài khoản → Đăng nhập**:

```text
Email: demo.path@quadlearn.local
Mật khẩu: Demo123456789
```

Chỉ dòng tên và vai trò `student`; không chọn **Dùng demo chỉ đọc**.

> “QuadLearn liên kết nội dung học, bài tập và tiến độ bằng Neo4j. Tôi sẽ trình bày một người học đang ở lớp 8, hoàn thành thêm nội dung rồi chuyển sang lớp 9 theo điều kiện của hệ thống.”

### Bước 2 — Trạng thái 50% và tiếp tục bài đang học

1. Mở **Tiến độ học tập**: lớp 8 có 4 bài, đã xong 2 bài, tỷ lệ 50%, điểm TB 10.
2. Chỉ **Tiếp tục: Hình thoi và đường chéo**.
3. Vào **Lộ trình học**, chọn lớp 8, chọn bài **Hình thoi và đường chéo**.
4. Xem các bài nền: Hình bình hành, song song, trung điểm, vuông góc…
5. Có thể chọn xem lớp 9 để thấy chưa đủ điều kiện, rồi quay lại lớp 8.

> “Có điểm 10 chưa đủ để chuyển cấp vì người học mới hoàn thành một nửa nội dung. Bài học hiện tại được liên kết đến kiến thức nền qua nhiều tầng graph. Việc bắt đầu học và việc hoàn thành học được lưu riêng.”

Bảng tiên quyết hiện dùng để hướng dẫn và truy xuất kiến thức; hệ thống chưa bắt buộc hoàn thành tất cả bài nền trước khi cho đánh dấu học xong bài hiện tại.

### Bước 3 — Xem nội dung và điều chỉnh hình

1. Mở **Nội dung & Hình học**, chọn lớp 8 và bài **Hình thoi và đường chéo**.
2. Tab **Lý thuyết** hiển thị nội dung; tab **Kiến thức nền** hiển thị các bài tiên quyết.
3. Mở tab **Thực hành hình học**, chọn **Hình chữ nhật**. Trong bảng thông số bên cạnh hình, đặt `a = 4`, `b = 3` → diện tích **12**, chu vi **14**.
4. Đổi sang **Hình thoi**: nhập cạnh `a = 4`, góc `α = 60°` → diện tích gần **13,9**, chu vi **16**. Công thức theo cạnh và góc là `S = a² × sin(α)`; công thức theo đường chéo trong bài học là `S = d1 × d2 / 2`.
5. Kéo một đỉnh để xem cạnh, góc và kết quả thay đổi. Nhập lại thông số để dựng lại hình ban đầu.

> “Mỗi hình có dữ kiện và công thức riêng. Người học có thể thay kích thước hoặc kéo đỉnh để quan sát các đại lượng và tính chất thay đổi.”

Bảng vẽ hiện có năm loại hình khởi đầu, nhập thông số và kéo thả đỉnh tự do. Đây là mô phỏng minh họa, chưa phải công cụ dựng hình đầy đủ. Đơn vị là `unit`, không tự coi là cm nếu bài không quy định.

### Bước 4 — Làm hai câu hình chữ nhật và lưu kết quả

1. Mở **Bài tập và trợ lý học tập**, kéo đến **Luyện tập trắc nghiệm**.
2. Chọn **Chủ đề = topic:8:rectangle**.
3. Chọn **4** cho câu “Hình chữ nhật có bao nhiêu góc vuông?”.
4. Chọn **Bằng nhau và cắt nhau tại trung điểm** cho câu về hai đường chéo.
5. Nhấn **Kiểm tra câu** nếu muốn xem giải thích từng câu.
6. Nhấn **Nộp bài luyện tập** → **10/10**; mở lại trang để xem lịch sử và chi tiết lần làm.

> “Kiểm tra câu là phản hồi tức thời; nộp bài mới lưu lần làm. Mỗi lần làm có các câu trả lời và option đã chọn. Hai câu đúng đều được tính điểm; với bộ này đúng một câu sẽ được 5/10.”

Tài khoản path đã có một lần làm 10 điểm; lần mới 10 điểm giữ trung bình ở 10. Không chọn đáp án sai trong flow chính. Để minh họa điểm yếu, dùng tài khoản review riêng.

### Bước 5 — Hoàn thành bài thứ ba và chuyển lớp

1. Trở lại **Lộ trình học**, chọn bài **Hình thoi và đường chéo**.
2. Nhấn **Tôi đã học xong bài này**.
3. Mở **Tiến độ học tập**, nhấn **Tính lại và lưu tiến độ**.
4. Chỉ kết quả lớp 8: **3/4 bài = 75%**, điểm TB **10**.
5. Mở **Hồ sơ và cấp độ**, chọn **Chuyển sang lớp = 9**.
6. **Không bật checkbox học vượt**, nhấn **Xác nhận đổi cấp độ**.
7. Mở lộ trình lớp 9; thấy bốn bài về nội tiếp, tính góc, nhận biết và ôn tập.

> “Điều kiện mặc định là hoàn thành ít nhất 70% và điểm trung bình ít nhất 6. Ba trên bốn bài bằng 75%, nên người học đã đủ điều kiện. Điểm bài làm do domain đánh giá lưu; domain lộ trình tổng hợp qua contract để quyết định truy cập cấp độ.”

Hoàn thành bài và điểm quiz độc lập: trả lời đúng không tự đánh dấu bài hoàn thành. Mặc định điểm TB tính tất cả các lần làm hoàn tất. Đạt ngưỡng khiến quyền truy cập được tính là hợp lệ; thao tác đổi cấp ghi nhận lớp hiện tại và cấp đã mở. Cột **Đã mở** có thể chưa đổi trước thao tác xác nhận.

### Bước 6 — Bài tập lớp 9 sau khi chuyển cấp

1. Vào **Nội dung & Hình học**, chọn lớp 9 → **Tứ giác nội tiếp**.
2. Giải thích bốn đỉnh cùng nằm trên một đường tròn; hai góc đối có tổng 180°.
3. Mở **Bài tập và trợ lý học tập**, chọn `topic:9:cyclic`.
4. Câu góc A = 70° → chọn **110°** cho góc C.
5. Câu số đỉnh trên cùng đường tròn → chọn **4**.
6. Nộp bài → **10/10** lớp 9. Mở Tiến độ và tính lại nếu muốn xem điểm cấp mới.

> “Bài tập đi theo lớp hiện tại của người dùng. Sau khi chuyển lớp, câu hỏi thay đổi từ tính chất hình chữ nhật sang tính chất nội tiếp. Hệ thống hiện có nội dung mẫu cho tất cả bốn cấp.”

### Bước 7 — Tự luận ba gợi ý và trợ lý mô phỏng

**Tự luận lớp 9:**

1. Ở **Bài tự luận**, chọn đề ABCD nội tiếp, A = 70°, B = 100°.
2. Nhấn **Mở gợi ý tiếp** lần lượt để xem: cặp góc đối → công thức → thay số.
3. Nhập `C = 180° − 70° = 110°; D = 180° − 100° = 80°`.
4. Nhấn **Xem lời giải đầy đủ**, chọn **Đã hiểu**, nhấn **Lưu tự đánh giá**.

Đây là lời giải mẫu và tự đánh giá, chưa tự chấm bài tự luận như giáo viên.

**Trợ lý:**

1. Chọn ngữ cảnh **Tứ giác nội tiếp**, ngôn ngữ `vi`.
2. Hỏi **“Tứ giác nội tiếp có những kiến thức tiên quyết nào?”** rồi nhấn **Gửi câu hỏi**.
3. Chỉ phản hồi, **Mở nguồn …**, lịch sử và lượt hỏi còn lại.

> “Hệ thống duyệt graph để lấy bài hiện tại và kiến thức nền. Provider hiện dùng mock, ghép tên nguồn, nội dung và hướng dẫn theo cấp. Đây là luồng truy xuất và lưu hội thoại đang hoạt động, chưa phải LLM có khả năng suy luận.”

Mock không thực sự phân tích câu hỏi, có thể dùng nội dung nguồn đầu tiên được trả về thay vì bài đang chọn. Hai câu khác nhau cùng ngữ cảnh có thể cho phản hồi giống nhau. Đừng dùng phản hồi mock để khẳng định một chứng minh mới là đúng. Quota mặc định 10 lượt/ngày; không cần API key.

### Bước 8 — Neo4j Browser

Chạy các query mục 5, dùng chế độ **Graph** cho đường đi và **Table** cho thống kê.

Ở query người học, đặt parameter:

```text
:param email => 'demo.path@quadlearn.local'
```

> “Hình vuông có hai hướng phân loại: chữ nhật và thoi. Một bài lớp 9 có nhiều lớp kiến thức nền. Neo4j lưu các quan hệ trực tiếp, giúp diễn đạt truy vấn đường đi tự nhiên. Riêng đăng nhập chủ yếu là lưu tài khoản/session; lợi thế graph rõ hơn ở quan hệ kiến thức và lộ trình.”

Không trả về toàn bộ node User khi chiếu màn hình vì nó có thuộc tính xác thực. Các query dưới chỉ trả thông tin cần trình bày.

### Bước 9 — Đổi tài khoản để xem tình huống khác

**Ôn tập:** đăng xuất path, đăng nhập `demo.review@quadlearn.local`, mở **Tiến độ học tập**. Chủ đề hình chữ nhật có TB 0; **Bài nền nên ôn** dẫn đến các tiên quyết chưa hoàn thành.

**Quản trị:** đăng nhập `demo.manager@quadlearn.local`, mở **Quản lý người dùng**, tìm `demo.start`. Nếu cần demo khóa/mở khóa, chỉ dùng tài khoản này; mở khóa lại sau thao tác. Khóa vô hiệu session cũ; người dùng phải đăng nhập lại sau mở khóa. Không khóa tài khoản đang trình bày hoặc admin hiện tại.

> “Các tài khoản được chuẩn bị ở những trạng thái khác nhau để thể hiện đủ tình huống, không phải thay đổi trạng thái bằng dữ liệu giả trên giao diện. Mỗi tình huống được đọc từ graph thật trên Neo4j local.”

## 3. Các flow mở rộng nếu giảng viên yêu cầu

### A. Đăng ký và kích hoạt tài khoản — thêm 2–3 phút

Thực hiện theo mục 1.2 ngay trên màn hình. Sau đăng ký, thử đăng nhập trước khi kích hoạt: tài khoản pending chưa được phép đăng nhập. Kích hoạt đủ mã rồi thử lại. Giải thích tại sao tài khoản được tạo và tài khoản được phép truy cập là hai trạng thái khác nhau.

### B. Bài kiểm tra tính giờ — thêm 2 phút

1. Đảm bảo người dùng hiện ở lớp 8.
2. Vào **Kiểm tra tính giờ**, chọn chủ đề hình chữ nhật, thời lượng **5 phút**.
3. Nhấn **Bắt đầu bài kiểm tra**, chọn đáp án 4 rồi nhấn **Lưu nháp**.
4. Chuyển sang trang khác, quay lại, chọn **Tiếp tục bài đang làm**.
5. Nhấn **Nộp bài kiểm tra**, xem điểm và lời giải; mở lại trang nếu cần để trở về trạng thái không có bài đang làm.

Đáp án/lời giải bị khóa trong lúc kiểm tra. Deadline được kiểm tra ở backend; đồng hồ hiển thị cập nhật khi Streamlit chạy lại trang, chưa phải bộ đếm tự cập nhật liên tục. Hết giờ, khi nộp hệ thống dùng đáp án đã lưu; không khẳng định có tác vụ tự nộp chạy nền lúc trình duyệt đóng. Hoàn tất bài đang làm trước khi đổi cấp hoặc chuyển sang demo chat.

### C. Gợi ý ôn tập từ điểm yếu — thêm 2 phút

Dùng **một học sinh mới khác ở lớp 8** để tránh làm thay đổi điểm của flow chính:

1. Chọn đáp án sai **2**, nộp bài luyện tập: điểm 0/10.
2. Vào **Tiến độ học tập**, xem **Điểm mạnh/yếu theo chủ đề** và **Bài nền nên ôn**.
3. Giải thích: chủ đề có điểm trung bình dưới 5 được xem là cần ôn; hệ thống tìm các bài tiên quyết chưa hoàn thành của bài thuộc chủ đề đó.

Gợi ý phụ thuộc lịch sử và các bài đã hoàn thành, nên có thể rỗng. Với một lần đúng 10 và một lần sai 0, trung bình là 5: **chưa nhỏ hơn 5**, không nên kỳ vọng sẽ được đánh dấu yếu. Bài nền cần ôn có thể ở cấp thấp hơn, không chỉ trong lớp hiện tại.

## 4. Kiến thức hình học nên nắm để giải thích

| Hình / khái niệm | Giải thích ngắn | Công thức / tính chất cần nhớ |
|---|---|---|
| Tứ giác | Đa giác có bốn cạnh | Với tứ giác lồi, tổng bốn góc trong là 360° |
| Hình bình hành | Tứ giác có hai cặp cạnh đối song song | Cạnh đối bằng nhau; hai đường chéo cắt nhau tại trung điểm; `S = a × h` |
| Hình chữ nhật | Hình bình hành có một góc vuông, suy ra bốn góc vuông | Hai đường chéo bằng nhau; `S = a × b`, `P = 2(a + b)` |
| Hình thoi | Tứ giác có bốn cạnh bằng nhau; là trường hợp riêng của hình bình hành | Hai đường chéo vuông góc; `S = d₁ × d₂ / 2`; hai đường chéo không nhất thiết bằng nhau |
| Hình vuông | Có bốn cạnh bằng nhau và bốn góc vuông | Vừa là hình chữ nhật vừa là hình thoi; `S = a²`, `P = 4a` |
| Hình thang cân | Hình thang có hai cạnh bên bằng nhau theo cách phân loại đang minh họa | Hai góc kề một đáy bằng nhau; `S = (a + b) × h / 2` |
| Tứ giác nội tiếp | Có bốn đỉnh cùng nằm trên một đường tròn | Với tứ giác lồi nội tiếp, tổng hai góc đối là 180° |
| Chiều cao | Khoảng cách vuông góc giữa đáy và đường thẳng chứa cạnh/đáy đối diện | Không thay chiều cao bằng cạnh nghiêng khi tính diện tích |

**Ba câu có thể dùng để tương tác với người xem:**

- “Hình chữ nhật có luôn là hình vuông không?” — Không; muốn là hình vuông phải có thêm các cạnh bằng nhau.
- “Hình vuông thuộc loại hình nào?” — Vừa thuộc hình chữ nhật vừa thuộc hình thoi, nên graph có hai cạnh phân loại đi ra.
- “Nếu chiều dài hình chữ nhật tăng gấp đôi, chiều rộng giữ nguyên thì sao?” — Diện tích gấp đôi; chu vi không nhất thiết gấp đôi.

Phân loại hình thang có thể khác tùy quy ước giáo trình. Graph hiện không khai báo hình bình hành `IS_A` hình thang; không suy diễn thêm quan hệ đó trong demo. Xem các vấn đề chưa chốt ở [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

## 5. Kiến thức Neo4j và các query dùng trong demo

### 5.1. Hiểu node, relationship, property

- **Node** biểu diễn một đối tượng: `User`, `Lesson`, `Quadrilateral`, `Question`, `Attempt`.
- **Label** chỉ loại node, ví dụ `Lesson`; **property** lưu dữ liệu đơn giản, ví dụ `id`, `title_vi`, `score`.
- **Relationship** biểu diễn mối liên hệ có hướng: bài cần bài nền, người học hoàn thành bài, lần làm có câu trả lời.
- **Cypher** là ngôn ngữ truy vấn graph. `MATCH` tìm mẫu quan hệ, `WHERE` lọc, `RETURN` chọn dữ liệu trả về.
- `*1..5` nghĩa là duyệt đường đi dài từ một đến năm quan hệ. Con số là giới hạn của query demo, không phải giới hạn chung của Neo4j.
- `MERGE` tìm hoặc tạo theo mẫu, kết hợp constraint ID duy nhất giúp tránh trùng node khi seed/chạy lại. Không phải cứ dùng `MERGE` là tự kiểm tra mọi quy tắc nghiệp vụ.
- **Transaction** gom các thao tác ghi liên quan: nếu một phần thất bại thì rollback cả nhóm thao tác trong transaction. Ví dụ lưu lần làm cùng chi tiết câu trả lời.

Các quan hệ chính:

```text
Level → HAS_CHAPTER → Chapter → HAS_TOPIC → Topic → HAS_LESSON → Lesson
Lesson → REQUIRES → Lesson
Quadrilateral → IS_A → Quadrilateral
User → STUDIES_AT → Level
User → COMPLETED → Lesson
User → HAS_PROGRESS → Progress → FOR_LEVEL → Level
User → ATTEMPTED → Attempt → HAS_ANSWER → AttemptAnswer
AttemptAnswer → ANSWERS → Question → HAS_OPTION → Option
AttemptAnswer → SELECTED → Option
User → HAS_CHAT → ChatSession → HAS_MESSAGE → ChatMessage
ChatSession → CONTEXT_LESSON → Lesson
```

Quan hệ `REQUIRES` đi từ bài **cần kiến thức nền** đến bài **cung cấp kiến thức nền**. Quan hệ `IS_A` đi từ loại hình cụ thể đến loại hình tổng quát hơn.

### Query 1 — Hình vuông thuộc những loại hình nào?

Dán vào Neo4j Browser, chọn chế độ **Graph**:

```cypher
MATCH p = (:Quadrilateral {id: 'shape:square'})-[:IS_A*1..5]->(:Quadrilateral)
RETURN p;
```

**Kỳ vọng:** thấy hình vuông nối đến hình chữ nhật và hình thoi; các đường đi dẫn tiếp đến hình bình hành, tứ giác. Một hình có thể thuộc nhiều loại: đây không phải cây chỉ có một cha.

### Query 2 — Kiến thức nền nhiều cấp của bài lớp 9

```cypher
MATCH p = (:Lesson {id: 'lesson:9:cyclic'})-[:REQUIRES*1..8]->(:Lesson)
RETURN p;
```

**Kỳ vọng:** từ tứ giác nội tiếp đến hình chữ nhật lớp 8, hình bình hành lớp 8, song song lớp 7 và hình chữ nhật trực quan lớp 6. Chuỗi này là mô hình demo, cần thẩm định khi bổ sung chương trình đầy đủ.

Muốn xem dạng bảng:

```cypher
MATCH p = (:Lesson {id: 'lesson:9:cyclic'})-[:REQUIRES*1..8]->(base:Lesson)
RETURN base.title_vi AS bai_nen, base.grade AS lop,
       min(length(p)) AS so_buoc
ORDER BY so_buoc;
```

**Ý nghĩa graph:** duyệt nhiều tầng mà không phải viết riêng một truy vấn cho mỗi lớp kiến thức.

### Query 3 — Lịch sử bài làm của người học vừa demo

Đặt parameter ở Neo4j Browser bằng email **thực tế đã đăng nhập**:

```text
:param email => 'email-hoc-sinh-demo@example.invalid'
```

Sau đó chạy:

```cypher
MATCH (u:User {email: $email})-[:ATTEMPTED]->(a:Attempt)
OPTIONAL MATCH (a)-[:FOR_TOPIC]->(t:Topic)
OPTIONAL MATCH (a)-[:HAS_ANSWER]->(ans:AttemptAnswer)
RETURN a.id AS lan_lam, t.name_vi AS chu_de, a.status AS trang_thai,
       a.score AS diem, count(DISTINCT ans) AS so_cau_tra_loi
ORDER BY lan_lam;
```

**Kỳ vọng:** có lần làm hoàn tất, điểm 10 và một câu trả lời từ bước 4. Nếu dùng admin để làm bài, thay parameter bằng `admin@quadlearn.local`. Dữ liệu mỗi người được phân biệt bằng node User và các quan hệ của người đó.

### Query 4 — Tiến độ đã tổng hợp

Giữ parameter email ở query 3. Trước khi chạy, vào giao diện **Tiến độ học tập → Tính lại và lưu tiến độ**:

```cypher
MATCH (u:User {email: $email})-[:HAS_PROGRESS]->(p:Progress)-[:FOR_LEVEL]->(l:Level)
RETURN l.grade AS lop, p.completion AS phan_tram,
       p.average_score AS diem_trung_binh
ORDER BY lop;
```

**Kỳ vọng:** lớp 8 có 75%, điểm trung bình 10 khi đi đúng flow trên. `Progress` là dữ liệu tổng hợp đã lưu; nguồn tính là các quan hệ hoàn thành và các lần làm. Sau khi có điểm mới, snapshot có thể cần cập nhật, dù một số bảng giao diện tính trực tiếp từ nguồn.

### Query 5 — Bài liên quan làm ngữ cảnh cho trợ lý

```cypher
MATCH p = (:Lesson {id: 'lesson:8:rectangle'})-[:REQUIRES|RELATED_TO*0..3]->(context:Lesson)
WHERE context.status = 'published'
RETURN DISTINCT context.id AS id, context.title_vi AS bai,
                context.grade AS lop
ORDER BY lop, id;
```

**Giải thích:** `0..3` gồm cả bài hiện tại và bài liên quan/tiên quyết trong ba bước. Đây là query minh họa ý tưởng truy xuất ngữ cảnh; tập nguồn thực tế trên UI còn phụ thuộc query và bộ lọc trong service hiện tại. Truy xuất graph là một phần chuẩn bị ngữ cảnh, chưa đủ để gọi hệ thống là RAG production.

Toàn bộ query trên chỉ đọc dữ liệu. Các query demo có sẵn khác nằm ở [database/examples.cypher](../database/examples.cypher), có thể chạy bằng `python -m scripts.db queries`.

### Vì sao dùng Neo4j trong bài này?

Các thực thể không chỉ đứng độc lập: bài có nhiều bài nền, hình có nhiều loại tổng quát, người học có nhiều lần làm. Quan hệ được lưu trực tiếp nên dễ diễn đạt bài toán “đi từ bài này đến kiến thức nền qua nhiều bước”. CSDL quan hệ cũng có thể giải quyết bằng join hoặc truy vấn đệ quy; lợi ích minh họa của Neo4j ở đây là mô hình và truy vấn phù hợp với cấu trúc liên kết, không phải khẳng định luôn nhanh hơn mọi database khác.

## 6. Hiểu sơ bộ code nào thực hiện phần đang demo

Luồng chung: **page → service/contract → repository → Database → Neo4j**. Page nhận thao tác và hiển thị; service áp dụng nghiệp vụ; repository chứa Cypher; Database quản lý kết nối và transaction.

| File / vùng code | Vai trò trong demo | Điều cần hiểu |
|---|---|---|
| `app/main.py` | Khởi chạy Streamlit, tập hợp navigation | Không gom toàn bộ nghiệp vụ vào đây |
| `app/core/navigation.py` | Đăng ký/tập hợp các trang feature | Thêm page qua registry của feature để hạn chế sửa file chung |
| `app/core/context.py` | Kết nối các thành phần của ba domain | Điểm nối quan trọng: cung cấp identity, content, assessment, progress cho page |
| `app/core/database.py` | Neo4j driver, `read`, `write`, `transaction` | Điểm kết nối DB dùng chung; không có một database khác cho từng domain |
| `app/shared/contracts/` | Các giao diện trao đổi giữa domain | Tránh import trực tiếp service/repository nội bộ của nhau |
| `identity_learning_path/services/auth.py` | Đăng ký, đăng nhập và luồng xác thực local | Logic tài khoản khác với UI nhập form |
| `identity_learning_path/services/learning_path.py` | `levels`, `access`, `change_level`, `complete_lesson`, `refresh`, `review_lessons` | Các hàm core cho tính tiến độ, chuyển cấp và gợi ý ôn tập |
| `identity_learning_path/repositories/` | Ghi/đọc người dùng và tiến độ | Module này sở hữu ghi tiến độ; không sở hữu chi tiết bài làm |
| `learning_geometry/pages/overview.py` | Tổ chức khu vực học tập | Chọn bài và ba tab; giữ kiểm tra cấp độ và link bài nguồn |
| `learning_geometry/pages/interactive_board.py` | Component mô phỏng HTML/SVG/JS | Hình vẽ, bảng thông số, kết quả và kéo đỉnh |
| `learning_geometry/repositories/` | Truy vấn nội dung và quan hệ kiến thức | Cung cấp bài học, tiên quyết và ngữ cảnh cho domain khác |
| `assessment_ai/pages/overview.py` | Trắc nghiệm, tự luận, chat và kiểm tra tính giờ | Các section khác nhau cùng thuộc trang bài tập hiện tại |
| `assessment_ai/services/quiz.py` | Chấm đáp án trắc nghiệm | Tính điểm dựa trên câu hỏi và option, không dựa trên trạng thái nút UI |
| `assessment_ai/services/mock_ai.py` | Provider trả lời mô phỏng | Điểm thay thế provider, không phải API LLM thật |
| `assessment_ai/repositories/` | Lưu lần làm, câu trả lời, hội thoại, tự đánh giá | Sở hữu dữ liệu chi tiết đánh giá và AI |
| `database/demo/content.json` | Nguồn học liệu, đáp án và tiên quyết của bộ demo mở rộng | 16 bài, 32 câu hỏi, 4 tự luận; chưa phải chương trình đầy đủ |
| `scripts/demo_data.py` | Import và tạo tài khoản/trạng thái demo | Tái dùng service để chấm bài và tính tiến độ; reset có phạm vi riêng |
| `database/seed.cypher` | Graph nền và taxonomy | Cần chạy trước trên database mới |
| `database/constraints.cypher` | Các constraint ID và ràng buộc dữ liệu | Giúp tránh trùng định danh; service vẫn phải kiểm tra nghiệp vụ |

Các đường dẫn feature ở bảng nằm dưới `app/features/`. Nếu cần giải thích sâu phần lộ trình, đọc [VU_NGHIEP_VU_VA_GIAI_THICH_CODE.md](VU_NGHIEP_VU_VA_GIAI_THICH_CODE.md). Thiết kế chung ở [ARCHITECTURE.md](ARCHITECTURE.md), [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md), [FEATURE_INTEGRATION.md](FEATURE_INTEGRATION.md).

**Ví dụ phối hợp cần nói được:** nội dung cung cấp danh sách bài đã xuất bản; đánh giá cung cấp lịch sử điểm; lộ trình dùng hai đầu vào đó cùng dữ liệu hoàn thành để tính tiến độ. Chỉ domain đánh giá ghi chi tiết `Attempt`; chỉ domain lộ trình ghi dữ liệu tổng hợp `Progress`. Cả hai dùng Neo4j local chung qua driver.

## 7. Câu hỏi thường gặp khi bảo vệ

**“Hoàn thành bài học được xác định bằng cách nào?”**

Hiện là người học tự nhấn nút hoàn thành. Hệ thống lưu quan hệ `COMPLETED`; không khẳng định đã kiểm chứng học sinh đọc hết bài hoặc hiểu hoàn toàn.

**“Tại sao làm đúng nhưng chưa lên lớp?”**

Cần cả tỷ lệ hoàn thành và điểm trung bình đạt ngưỡng. Kiểm tra đang có bao nhiêu bài đã xuất bản, đã hoàn thành mấy bài, đã nộp bài hay mới kiểm tra từng câu, và lịch sử có điểm thấp không.

**“AI có gọi ChatGPT không?”**

Không. Provider hiện là mock. Hệ thống đã có truy xuất nội dung, nguồn tham chiếu, lưu hội thoại và quota; chưa tích hợp LLM thật.

**“Mã kích hoạt gửi qua email chưa?”**

Chưa. Demo local hiển thị mã trong ứng dụng. Email/OAuth và xác thực người giám hộ thực tế cần triển khai thêm.

**“Có đủ bài lớp 6–9 chưa?”**

Chưa. Có các cấp và dữ liệu đại diện để chứng minh liên kết. Bộ demo mở rộng có 16 bài học, 32 câu trắc nghiệm và 4 bài tự luận, phủ cả bốn cấp. Mỗi cấp có 4 bài học, 8 câu hỏi và 1 bài tự luận; chưa phải chương trình đầy đủ.

**“Điểm có mất sau khi tắt ứng dụng không?”**

Dữ liệu ghi vào Neo4j được giữ trong Docker named volume. Tắt Streamlit hoặc `docker compose stop` không xóa volume. Các lệnh xóa volume/reset dữ liệu là thao tác riêng cần cẩn thận.

**“Ba thành viên chia việc thế nào?”**

Vũ phụ trách danh tính, lộ trình và tiến độ; Sơn phụ trách nội dung, quan hệ kiến thức và hình học; Đạt phụ trách bài làm, tự luận và trợ lý. Các domain trao đổi qua contract chung và có quyền sở hữu thao tác ghi rõ ràng. Chi tiết ở [DOMAIN_OWNERSHIP.md](DOMAIN_OWNERSHIP.md).

## 8. Xử lý tình huống trong buổi demo

| Tình huống | Kiểm tra / cách xử lý |
|---|---|
| Không mở được trang 8501 | Kiểm tra Terminal chạy Streamlit; nếu đã đổi port thì dùng URL được in ở Terminal |
| Không kết nối Neo4j | Chạy `docker compose ps`, `docker compose logs neo4j`, `python -m scripts.db check`; kiểm tra Docker và `.env` |
| Lỗi thiếu method sau khi cập nhật code, ví dụ `Database.transaction` | Dừng tiến trình Streamlit cũ bằng Ctrl+C rồi khởi động lại để nạp class mới |
| Không lưu được / nút bị khóa | Kiểm tra đang dùng demo chỉ đọc, chưa đăng nhập, hoặc có bài kiểm tra đang làm |
| Đăng nhập tài khoản mới thất bại | Kiểm tra trạng thái pending, mã kích hoạt và xác nhận người giám hộ nếu cần |
| Không thấy trắc nghiệm sau khi đổi lớp 9 | Bộ demo mở rộng có câu hỏi lớp 6–9; kiểm tra đã chạy scripts.demo_data và đang chọn đúng lớp/chủ đề |
| Không đủ điều kiện lớp 9 | Kiểm tra ít nhất 3/4 bài lớp 8 (75%), điểm trung bình ≥6, đã nộp bài; không bật học vượt để che việc chưa đạt |
| Query người học trả rỗng | Thay `$email` bằng đúng email đã demo; kiểm tra thao tác đã được lưu |
| Chat không gửi được | Kiểm tra quota, câu hỏi thuộc hình học và không có bài kiểm tra đang làm |
| Gợi ý ôn tập rỗng | Kiểm tra điểm trung bình chủ đề có dưới 5 và còn bài tiên quyết chưa hoàn thành hay không |

**Flow rút gọn 5–7 phút:** đăng nhập → xem tiên quyết → hình chữ nhật 4×3 → nộp đáp án 4 → xem tiến độ → chạy graph hình vuông và graph tiên quyết. Bỏ đăng ký, kiểm tra tính giờ, tự luận và admin nếu thời gian ngắn; không nói đã demo các phần bị bỏ.

**Nếu database không khả dụng:** có thể trình bày kiến trúc và query trong tài liệu, nhưng nói rõ chưa chạy được luồng lưu dữ liệu trong buổi đó. Không báo PASS hoặc dùng dữ liệu hardcode thay cho kết quả database.

Kết thúc buổi demo: Ctrl+C ở Terminal để dừng Streamlit; có thể dùng `docker compose stop` để dừng Neo4j. **Không dùng `docker compose down -v`** nếu muốn giữ dữ liệu. Hướng dẫn vận hành đầy đủ ở [RUN_PROJECT.md](RUN_PROJECT.md); tình trạng kiểm chứng và giới hạn nghiệp vụ ở [POST_MERGE_AUDIT_2026-10-09.md](POST_MERGE_AUDIT_2026-10-09.md).

## 9. Kiểm tra tài liệu khi bàn giao

- **PASS:** sáu khối Cypher trong mục 5 (gồm bản graph và bản bảng của query tiên quyết) đã thực thi thành công trên Neo4j local ngày 09/10/2026, chỉ đọc dữ liệu.
- **PASS:** các liên kết tài liệu local tồn tại; kiểm tra định dạng diff không có lỗi whitespace.
- **PASS:** 191 tests (179 unit/UI + 12 integration), bảy tài khoản và luồng service 50% → 75% → lớp 9 trên DB thật.
- **PASS:** năm trang Streamlit render bằng AppTest với DB thật; fixture đã phục hồi về trạng thái ban đầu.
- **Đã đối chiếu source:** tên màn hình/nút, dữ liệu, công thức và chính sách chuyển cấp mặc định.
- **CHƯA KIỂM CHỨNG trong lần viết tài liệu này:** thao tác trực tiếp toàn bộ flow bằng trình duyệt và chạy các lệnh trên Windows. Người trình bày cần chạy thử checklist trước buổi demo.

Query lịch sử/tiến độ có thể trả rỗng nếu tài khoản được chọn chưa có dữ liệu tương ứng. Việc query chạy thành công xác nhận cú pháp và schema hiện tại; không thay thế việc kiểm tra kết quả sau từng thao tác UI của flow.
