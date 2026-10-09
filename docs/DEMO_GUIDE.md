# QuadLearn — Hướng dẫn demo và kiến thức cần hiểu

Tài liệu dành cho người trực tiếp trình bày bài tập Neo4j. Flow chính mất khoảng **15–20 phút**, đi theo hành trình của một người học: đăng nhập → học lý thuyết → xem hình → làm bài → theo dõi tiến độ → chuyển cấp → hỏi trợ lý → xem graph.

Đối chiếu với giao diện và dữ liệu demo trong repository ngày **09/10/2026**. Dữ liệu chỉ minh họa một số nội dung lớp 6–9; các kết quả dưới đây giả định đã chạy seed và dùng chính sách mặc định. Có thể đọc lời thuyết trình gợi ý rồi diễn đạt lại bằng lời của mình.

## 1. Chuẩn bị trước khi trình bày

### 1.1. Mở ứng dụng và database

Nếu ứng dụng đã chạy, mở <http://localhost:8501>. Neo4j Browser ở <http://localhost:7474>.

**macOS**, mở Terminal tại thư mục project đã setup:

```bash
source .venv/bin/activate
docker compose up -d --wait
python -m scripts.db check
python -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501
```

**Windows PowerShell**, tại thư mục project đã setup:

```powershell
.\.venv\Scripts\Activate.ps1
docker compose up -d --wait
python -m scripts.db check
python -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501
```

Máy mới cần làm theo [Windows](SETUP_WINDOWS.md) hoặc [macOS](SETUP_MACOS.md), tạo `.env` và cài dependencies trước. Nếu chưa có dữ liệu, chạy `python -m scripts.db init` trước lệnh Streamlit. Không cần chạy seed lại mỗi lần demo.

Trong Neo4j Browser, kết nối `bolt://localhost:7687`, dùng `NEO4J_USER` và `NEO4J_PASSWORD` của `.env`. **Đăng nhập Neo4j khác đăng nhập QuadLearn**: một bên truy cập database, một bên là tài khoản ứng dụng. Không chiếu `.env`, mật khẩu hoặc dữ liệu xác thực lên màn hình.

### 1.2. Chọn tài khoản đúng với flow

| Tài khoản | Dùng để làm gì | Điểm cần nhớ |
|---|---|---|
| Học sinh mới, khởi đầu lớp 8 | Flow chính từ 0% đến chuyển lớp 9 | Khuyến nghị chuẩn bị trước buổi demo để kết quả dễ dự đoán |
| `admin@quadlearn.local` | Đăng nhập nhanh, demo quản lý người dùng | Đã tạo trên database local hiện tại; mật khẩu đã được cấp riêng. Không phải tài khoản có sẵn trong seed trên mọi máy |
| `student@example.invalid` / nút **Dùng demo chỉ đọc** | Xem nội dung và dữ liệu minh họa | Không có mật khẩu đăng nhập seed; không dùng để lưu bài làm, chat hoặc tiến độ |

**Tạo học sinh demo trước buổi trình bày:** vào **Tài khoản → Đăng ký**, dùng email mới, tên tùy chọn, mật khẩu có chữ và số từ 8 ký tự, chọn lớp 8. Có thể dùng người học thử nghiệm 18 tuổi để chỉ cần một mã kích hoạt. Vào **Kích hoạt tài khoản**, chọn `verify`, nhập mã hiển thị sau đăng ký rồi đăng nhập. Tài khoản mới luôn có vai trò `student`.

Nếu minh họa người học dưới 16 tuổi, nhập thêm email người giám hộ và thực hiện cả mã `verify` lẫn `guardian`. Đây là luồng xác thực **local**: mã hiển thị trong ứng dụng, chưa gửi email thật và chưa xác minh sự đồng ý thực tế của người giám hộ. Dùng dữ liệu thử nghiệm, không nhập thông tin trẻ em thật.

Chuẩn bị thêm một cửa sổ riêng cho admin nếu muốn chuyển qua màn quản trị. Không đăng xuất học sinh giữa flow chính nếu chưa ghi nhớ thông tin đăng nhập.

### 1.3. Checklist chạy thử

- [ ] Neo4j đang chạy; lệnh `python -m scripts.db check` báo `Neo4j connection OK`.
- [ ] Trang chủ và các mục menu mở được.
- [ ] Học sinh demo đang ở lớp 8, chưa hoàn thành bài và chưa có điểm.
- [ ] Lớp 8 có hai bài: **Hình bình hành** và **Hình chữ nhật và tính chất**.
- [ ] Có câu hỏi **Hình chữ nhật có bao nhiêu góc vuông?**, đáp án **4**.
- [ ] Không có bài kiểm tra tính giờ còn đang làm; nếu có, hoàn tất và nộp trước.
- [ ] Trợ lý còn lượt hỏi; chuẩn bị câu hỏi về tứ giác.
- [ ] Đã mở sẵn Neo4j Browser và thử các query ở mục 5.

Các bước làm bài và đánh dấu hoàn thành **ghi dữ liệu thật vào database local**. Muốn diễn lại trạng thái 0%, tạo học sinh mới. Không xóa dữ liệu cả nhóm hoặc chạy reset chỉ để làm lại một flow.

## 2. Flow chính: thao tác, kết quả và lời trình bày

### Tổng quan thời gian

| Bước | Màn hình | Thời gian | Điều cần chứng minh |
|---|---|---:|---|
| 1 | Trang chủ, Tài khoản | 1 phút | Mục tiêu hệ thống và danh tính người học |
| 2 | Lộ trình học | 2 phút | Phân cấp chương/bài, kiến thức tiên quyết, tiếp tục học |
| 3 | Nội dung & Hình học | 2 phút | Lý thuyết đi cùng mô phỏng và công thức |
| 4 | Bài tập và trợ lý học tập | 2 phút | Chấm trắc nghiệm và lưu lịch sử |
| 5 | Tiến độ học tập, Hồ sơ và cấp độ | 3 phút | Tổng hợp giữa domain, điều kiện chuyển cấp |
| 6 | Bài tập và trợ lý học tập | 2 phút | Tự luận, gợi ý và tự đánh giá |
| 7 | Bài tập và trợ lý học tập | 2 phút | Trợ lý mô phỏng dùng ngữ cảnh graph |
| 8 | Neo4j Browser | 3 phút | Quan hệ nhiều cấp và dữ liệu đã lưu |
| 9 | Quản lý người dùng, kết thúc | 1 phút | Vai trò admin và giới hạn hiện tại |

### Bước 1 — Giới thiệu và đăng nhập

**Thao tác**

1. Mở **Trang chủ**.
2. Chỉ các mục học tập, lộ trình và bài tập trên menu.
3. Vào **Tài khoản → Đăng nhập**, đăng nhập học sinh lớp 8 đã chuẩn bị.
4. Chỉ dòng `Đang dùng: … · student`.

**Kết quả mong đợi:** ứng dụng nhận đúng người dùng. Không chọn **Dùng demo chỉ đọc** cho flow có thao tác lưu.

**Lời trình bày gợi ý**

> “QuadLearn hỗ trợ học tứ giác theo cấp độ lớp 6 đến lớp 9. Người học xem lý thuyết, tương tác với hình, làm bài và theo dõi tiến độ. Dữ liệu được lưu trong Neo4j, đặc biệt là các quan hệ giữa bài học, kiến thức nền và các loại tứ giác.”

**Kiến thức phần mềm:** xác thực trả lời “bạn là ai”; phân quyền trả lời “bạn được phép làm gì”. Tài khoản ứng dụng có mật khẩu được băm và session lưu trong Neo4j. Quyền ghi được kiểm tra ở lớp nghiệp vụ, ngoài việc ẩn hoặc khóa nút trên giao diện.

### Bước 2 — Xem lộ trình và kiến thức tiên quyết

**Thao tác**

1. Vào **Lộ trình học**, chọn **Lớp xem lộ trình = 8**.
2. Mở chương để xem chủ đề và hai bài học.
3. Chọn **Hình chữ nhật và tính chất** ở **Bài học**.
4. Chỉ bảng bài nền: hình bình hành, hai đường thẳng song song và hình chữ nhật trực quan.
5. Nhấn **Bắt đầu / tiếp tục bài này**.
6. Sang **Tiến độ học tập**, chỉ thông tin **Tiếp tục: Hình chữ nhật và tính chất**.

**Kết quả mong đợi:** bài đang học được ghi nhận; bắt đầu bài chưa làm tăng số bài hoàn thành. Người học có thể quay lại bài đó.

**Lời trình bày gợi ý**

> “Hình chữ nhật ở lớp 8 có liên hệ với hình bình hành. Muốn hiểu hình bình hành thì cần hiểu các cặp cạnh song song. Hệ thống có thể đi qua nhiều quan hệ để tìm toàn bộ kiến thức nền, thay vì chỉ lấy một bài trước đó.”

**Điểm cần phân biệt:** bảng tiên quyết giúp hướng dẫn học và truy xuất kiến thức. Hiện tại việc hoàn thành mọi bài tiên quyết chưa được dùng làm điều kiện bắt buộc cho nút **Tôi đã học xong bài này**. Điều kiện truy cập cấp độ là cơ chế riêng, minh họa ở bước 5.

### Bước 3 — Lý thuyết và mô phỏng hình học

**Thao tác**

1. Vào **Nội dung & Hình học**, chọn khối lớp 8.
2. Chọn bài **Hình chữ nhật và tính chất**.
3. Trong **Chọn hình tứ giác mô phỏng**, chọn **Hình chữ nhật**.
4. Đặt chiều dài `a = 4`, chiều rộng `b = 3`.
5. Chỉ hình, công thức và kết quả: diện tích **12 unit²**, chu vi **14 unit**.
6. Tăng `a` từ 4 lên 6: diện tích thành **18**, chu vi thành **18**.
7. Nếu còn thời gian, đổi sang hình bình hành: `a = 6`, `h = 4`, diện tích **24**.

**Lời trình bày gợi ý**

> “Hình chữ nhật có bốn góc vuông. Diện tích bằng chiều dài nhân chiều rộng; chu vi là hai lần tổng hai cạnh kề. Với hình bình hành, diện tích dùng chiều cao vuông góc với đáy, không dùng cạnh nghiêng.”

**Giới hạn trình bày:** giao diện hiện có mô phỏng SVG điều chỉnh bằng slider cho năm loại hình. Không giới thiệu đây là công cụ dựng hình hoàn chỉnh hoặc giao diện kéo thả đỉnh tự do. Đơn vị trên màn hình là `unit`; chỉ quy đổi thành cm khi bài toán quy định đơn vị.

### Bước 4 — Trắc nghiệm và lịch sử bài làm

**Thao tác**

1. Vào **Bài tập và trợ lý học tập**, kéo xuống **Luyện tập trắc nghiệm**.
2. Chọn **Chủ đề = topic:8:rectangle**.
3. Với câu **Hình chữ nhật có bao nhiêu góc vuông?**, chọn **4**.
4. Nhấn **Kiểm tra câu** để xem phản hồi đúng và giải thích.
5. Nhấn **Nộp bài luyện tập** để lưu lần làm.
6. Xem điểm **10/10**, sau đó chọn lần làm ở **Xem lại lần làm**. Nếu danh sách chưa cập nhật ngay, mở lại trang.

**Kết quả mong đợi:** một lần làm đã hoàn tất, có điểm và chi tiết đáp án được lưu. Với bộ seed hiện tại, chủ đề này có một câu nên trả lời đúng đạt 10/10. Đây là dữ liệu minh họa, không phải một đề kiểm tra đầy đủ.

**Lời trình bày gợi ý**

> “Kiểm tra từng câu giúp học sinh nhận phản hồi ngay. Nộp bài mới lưu lịch sử làm bài. Một lần làm liên kết đến người học, chủ đề, câu hỏi và đáp án đã chọn. Phần tiến độ dùng kết quả này để tính điểm trung bình.”

Không nộp thêm đáp án sai trong flow chính: chính sách mặc định tính trung bình tất cả các lần làm hoàn tất, nên lần làm mới có thể thay đổi điều kiện chuyển cấp.

### Bước 5 — Từ tiến độ đến chuyển lớp 9

Đây là bước thể hiện rõ sự tích hợp giữa nội dung, bài làm và lộ trình.

**Thao tác**

1. Vào **Lộ trình học**, lớp 8, chọn **Hình chữ nhật và tính chất**.
2. Nhấn **Tôi đã học xong bài này**.
3. Vào **Tiến độ học tập**, nhấn **Tính lại và lưu tiến độ**.
4. Chỉ lớp 8: **1/2 bài = 50%**, điểm trung bình **10**.
5. Chọn xem lộ trình lớp 9: với học sinh mới, cấp này chưa đủ điều kiện truy cập.
6. Quay lại lộ trình lớp 8, chọn **Hình bình hành**, đánh dấu học xong.
7. Vào **Tiến độ học tập**, tính lại và lưu: **2/2 bài = 100%**, điểm trung bình **10**.
8. Vào **Hồ sơ và cấp độ**, chọn **Chuyển sang lớp = 9**.
9. Để checkbox học vượt ở trạng thái bỏ chọn; nhấn **Xác nhận đổi cấp độ**.
10. Vào **Lộ trình học**, chọn lớp 9 và mở bài **Tứ giác nội tiếp**.

**Giải thích điều kiện mặc định**

- Hoàn thành ít nhất **70%** số bài đã xuất bản của cấp trước.
- Điểm trung bình của các lần làm hoàn tất ở cấp trước ít nhất **6/10**.
- Chỉ có điểm 10 nhưng mới hoàn thành 50% thì chưa đủ điều kiện.
- Với hai bài seed lớp 8, tỷ lệ chỉ có thể là 0%, 50% hoặc 100%; phải xong cả hai mới đạt ngưỡng 70%.
- Bài học hoàn thành và điểm bài làm là hai dữ liệu độc lập. Trả lời đúng trắc nghiệm không tự đánh dấu bài học hoàn thành.

**Lời trình bày gợi ý**

> “Tiến độ không chỉ là điểm kiểm tra. Người học cần vừa học đủ nội dung vừa đạt điểm tối thiểu. Kết quả bài làm được module đánh giá lưu; module lộ trình đọc kết quả và nội dung qua contract để tổng hợp, tránh hai module cùng ghi một nghiệp vụ.”

**Lưu ý trạng thái:** khi đạt ngưỡng, quyền truy cập lớp 9 có thể được tính là hợp lệ trước khi đổi lớp. Cột **Đã mở** phản ánh cấp đã mở/đã ghi nhận; thao tác **Xác nhận đổi cấp độ** cập nhật lớp hiện tại và ghi nhận việc mở cấp. Đừng lấy riêng cột này để kết luận việc tính điều kiện sai.

Chính sách có thể được thay đổi qua biến `VU_UNLOCK_COMPLETION`, `VU_UNLOCK_SCORE`, `VU_AVERAGE_POLICY`, `VU_ALLOW_SKIP`; tài liệu dùng mặc định 70%, 6, `all`, cho phép học vượt có xác nhận. Học vượt là luồng có cảnh báo và xác nhận riêng, không dùng ở bước này để chứng minh đạt ngưỡng.

### Bước 6 — Tự luận và gợi ý từng bước

**Thao tác**

1. Trong **Hồ sơ và cấp độ**, đổi về lớp 8. Cấp thấp hơn đã có quyền truy cập.
2. Mở **Bài tập và trợ lý học tập**, kéo xuống **Bài tự luận**.
3. Chọn đề **Tính diện tích hình chữ nhật có chiều dài 4 cm, chiều rộng 3 cm.**
4. Nhấn **Mở gợi ý tiếp**, chỉ gợi ý `S = a × b`.
5. Nhập bài làm: `S = 4 × 3 = 12 cm²`.
6. Nhấn **Xem lời giải đầy đủ**, so sánh bài làm với lời giải mẫu.
7. Chọn **Đã hiểu** ở **Tự đánh giá**, nhấn **Lưu tự đánh giá**.

**Lời trình bày gợi ý**

> “Bài tự luận cho người học xem giả thiết, kết luận và mở gợi ý khi cần. Sau khi đối chiếu lời giải, người học tự đánh giá mức hiểu. Hệ thống lưu bài làm, số gợi ý đã dùng và kết quả tự đánh giá.”

Bộ seed này có **một gợi ý**. Không nói đã có nhiều bước cho mọi đề. Phần này chưa tự chấm bài tự luận như giáo viên và không tự chuyển kết quả tự đánh giá thành điểm trắc nghiệm.

### Bước 7 — Trợ lý mô phỏng và nguồn kiến thức

**Thao tác**

1. Trong **Bài tập và trợ lý học tập**, tìm **Trợ lý học tập · bản mô phỏng**.
2. Chọn **Ngữ cảnh bài học = Hình chữ nhật và tính chất**, ngôn ngữ `vi`.
3. Nhập: **Vì sao hình chữ nhật là hình bình hành?**
4. Nhấn **Gửi câu hỏi**.
5. Chỉ câu trả lời, các liên kết **Mở nguồn …** và số lượt còn lại.
6. Mở một nguồn để xem bài học được liên kết. Quay lại trang bài tập.
7. Xem **Lịch sử chat**; có thể chọn **Hữu ích** và nhấn **Lưu đánh giá**.

**Lời trình bày gợi ý**

> “Ứng dụng truy xuất bài học hiện tại và kiến thức liên quan trong graph để tạo ngữ cảnh. Mỗi câu trả lời có thể dẫn về bài nguồn. Nhà cung cấp trả lời hiện là mock để demo không cần API key; nhóm đã có điểm tích hợp để thay bằng provider thật sau này.”

**Phải nói đúng:** câu trả lời mô phỏng không có năng lực suy luận của LLM và có thể không giải thích đầy đủ câu hỏi cụ thể. Phần có thể chứng minh ở đây là truy xuất ngữ cảnh, liên kết nguồn, lưu hội thoại và giới hạn lượt hỏi. Mặc định quota là 10 lượt/ngày, có thể khác nếu cấu hình thay đổi; không cố hỏi hết quota trong flow chính.

### Bước 8 — Cho thấy dữ liệu graph thực tế

Chuyển sang Neo4j Browser, chạy query 1–4 ở mục 5. Mỗi query chỉ giải thích một ý: phân loại hình, kiến thức nền nhiều cấp, lịch sử bài làm và tiến độ.

**Lời trình bày gợi ý**

> “Ở đây các quan hệ có ý nghĩa nghiệp vụ. Hình vuông vừa là hình chữ nhật vừa là hình thoi. Một bài lớp 9 có thể cần kiến thức lớp 8, lớp 7 và lớp 6. Neo4j cho phép duyệt các đường đi đó trực tiếp bằng Cypher.”

Dùng chế độ Graph cho query trả về đường đi; dùng Table cho query thống kê. Không trả về toàn bộ node `User` khi chiếu màn hình, vì thuộc tính người dùng có thể chứa dữ liệu xác thực.

### Bước 9 — Vai trò admin và kết thúc

Nếu có thời gian, chuyển sang cửa sổ admin đã đăng nhập, vào **Quản lý người dùng**, nhập tên/email học sinh demo tại **Tìm theo tên/email**.

Chỉ danh sách và điều khiển **Khóa tài khoản được chọn → Áp dụng khóa / mở khóa**. Nếu thực sự demo thao tác khóa, dùng tài khoản thử nghiệm khác, sau đó mở khóa lại. Khóa tài khoản vô hiệu session cũ; cần đăng nhập lại sau khi được mở khóa. Không khóa học sinh đang dùng trong flow hoặc tài khoản admin hiện tại.

**Lời kết gợi ý**

> “Qua một hành trình học, nhóm đã kết nối nội dung, đánh giá và tiến độ trong cùng graph. Neo4j hỗ trợ mô hình quan hệ kiến thức; ứng dụng dùng các domain riêng để phát triển song song. Phiên bản hiện tại có nội dung mẫu và AI mô phỏng; bộ chương trình đầy đủ, email thật và LLM thật là các phần cần phát triển tiếp.”

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

**Kỳ vọng:** lớp 8 có 100%, điểm trung bình 10 khi đi đúng flow trên. `Progress` là dữ liệu tổng hợp đã lưu; nguồn tính là các quan hệ hoàn thành và các lần làm. Sau khi có điểm mới, snapshot có thể cần cập nhật, dù một số bảng giao diện tính trực tiếp từ nguồn.

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
| `learning_geometry/pages/overview.py` | Lý thuyết và mô phỏng đang nhìn thấy | Năm hình điều chỉnh bằng slider trên trang hiện tại |
| `learning_geometry/repositories/` | Truy vấn nội dung và quan hệ kiến thức | Cung cấp bài học, tiên quyết và ngữ cảnh cho domain khác |
| `assessment_ai/pages/overview.py` | Trắc nghiệm, tự luận, chat và kiểm tra tính giờ | Các section khác nhau cùng thuộc trang bài tập hiện tại |
| `assessment_ai/services/quiz.py` | Chấm đáp án trắc nghiệm | Tính điểm dựa trên câu hỏi và option, không dựa trên trạng thái nút UI |
| `assessment_ai/services/mock_ai.py` | Provider trả lời mô phỏng | Điểm thay thế provider, không phải API LLM thật |
| `assessment_ai/repositories/` | Lưu lần làm, câu trả lời, hội thoại, tự đánh giá | Sở hữu dữ liệu chi tiết đánh giá và AI |
| `database/seed.cypher` | Bộ nội dung và quan hệ demo | Không phải toàn bộ chương trình lớp 6–9 |
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

Chưa. Có các cấp và dữ liệu đại diện để chứng minh liên kết. Seed có một bài ở lớp 6, một bài ở lớp 7, hai bài ở lớp 8 và một bài ở lớp 9. Bộ trắc nghiệm/tự luận seed tập trung lớp 8.

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
| Không thấy trắc nghiệm sau khi đổi lớp 9 | Seed trắc nghiệm chỉ ở lớp 8; đổi lớp hiện tại về 8 trong Hồ sơ |
| Không đủ điều kiện lớp 9 | Kiểm tra 2/2 bài lớp 8, điểm trung bình ≥6, đã nộp bài; không bật học vượt để che việc chưa đạt |
| Query người học trả rỗng | Thay `$email` bằng đúng email đã demo; kiểm tra thao tác đã được lưu |
| Chat không gửi được | Kiểm tra quota, câu hỏi thuộc hình học và không có bài kiểm tra đang làm |
| Gợi ý ôn tập rỗng | Kiểm tra điểm trung bình chủ đề có dưới 5 và còn bài tiên quyết chưa hoàn thành hay không |

**Flow rút gọn 5–7 phút:** đăng nhập → xem tiên quyết → hình chữ nhật 4×3 → nộp đáp án 4 → xem tiến độ → chạy graph hình vuông và graph tiên quyết. Bỏ đăng ký, kiểm tra tính giờ, tự luận và admin nếu thời gian ngắn; không nói đã demo các phần bị bỏ.

**Nếu database không khả dụng:** có thể trình bày kiến trúc và query trong tài liệu, nhưng nói rõ chưa chạy được luồng lưu dữ liệu trong buổi đó. Không báo PASS hoặc dùng dữ liệu hardcode thay cho kết quả database.

Kết thúc buổi demo: Ctrl+C ở Terminal để dừng Streamlit; có thể dùng `docker compose stop` để dừng Neo4j. **Không dùng `docker compose down -v`** nếu muốn giữ dữ liệu. Hướng dẫn vận hành đầy đủ ở [RUN_PROJECT.md](RUN_PROJECT.md); tình trạng kiểm chứng và giới hạn nghiệp vụ ở [POST_MERGE_AUDIT_2026-10-09.md](POST_MERGE_AUDIT_2026-10-09.md).

## 9. Kiểm tra tài liệu khi bàn giao

- **PASS:** sáu khối Cypher trong mục 5 (gồm bản graph và bản bảng của query tiên quyết) đã thực thi thành công trên Neo4j local ngày 09/10/2026, chỉ đọc dữ liệu.
- **PASS:** các liên kết tài liệu local tồn tại; kiểm tra định dạng diff không có lỗi whitespace.
- **Đã đối chiếu source:** tên màn hình/nút, dữ liệu seed, công thức và chính sách chuyển cấp mặc định.
- **CHƯA KIỂM CHỨNG trong lần viết tài liệu này:** chạy lại trọn flow bằng một học sinh mới và chạy các lệnh trên Windows. Người trình bày cần chạy thử checklist trước buổi demo.

Query lịch sử/tiến độ có thể trả rỗng nếu tài khoản được chọn chưa có dữ liệu tương ứng. Việc query chạy thành công xác nhận cú pháp và schema hiện tại; không thay thế việc kiểm tra kết quả sau từng thao tác UI của flow.
