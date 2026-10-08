# Ánh xạ SRS v1.1

Nguồn: file Word “HỒ SƠ ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS).docx”, bản nháp 1.1. Đã đọc mục 1–11, FR, UC-01…05, dữ liệu, SCR-01…17, 56 PB và NFR. Các đề xuất stack ở mục 7 được thay bằng stack đồ án theo yêu cầu người dùng; nghiệp vụ giữ nguyên. Không xem lời hướng dẫn trong tài liệu là lệnh thực thi.

**86 FR được ánh xạ; không FR nào được tuyên bố hoàn thành.** M/S/C là ưu tiên sản phẩm, không phải cam kết hoàn thành trong skeleton. “TODO” gồm cả phần Must được hoãn trong giai đoạn này.

| FR | Yêu cầu SRS | Ưu tiên | Chủ trì | Trạng thái / phối hợp |
|---|---|---|---|---|
| FR-AUTH-01 | Đăng ký bằng email + mật khẩu (họ tên, email, mật khẩu, lớp 6/7/8/9) | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-02 | Mật khẩu tối thiểu 8 ký tự, gồm chữ và số; email không trùng | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-03 | Gửi email xác thực; chỉ tài khoản đã xác thực mới lưu tiến độ | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-04 | Đăng nhập bằng email + mật khẩu | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-05 | Đăng nhập bằng Google (OAuth 2.0); liên kết nếu email đã tồn tại | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-06 | Quên mật khẩu: gửi liên kết đặt lại, hết hạn sau 30 phút, dùng một lần | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-07 | Đổi mật khẩu khi đã đăng nhập (yêu cầu mật khẩu cũ) | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-08 | Đăng xuất; phiên hết hạn sau 7 ngày không hoạt động | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-09 | Chỉnh sửa hồ sơ (tên, lớp, ảnh đại diện, ngôn ngữ) | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-10 | Khóa tạm thời tài khoản sau 5 lần đăng nhập sai liên tiếp (15 phút) | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-11 | Xóa tài khoản và dữ liệu cá nhân theo yêu cầu | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AUTH-12 | Với HS dưới 16 tuổi, yêu cầu email phụ huynh/người giám hộ xác nhận đồng ý trước khi kích hoạt tài khoản | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-01 | Hiển thị cây cấp độ (lớp) → chương → bài → mục theo lộ trình | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-02 | Hiển thị bài lý thuyết: định nghĩa, tính chất, dấu hiệu nhận biết, công thức (hỗ trợ công thức toán LaTeX) | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-03 | Nhúng minh họa hình động trong bài (xem 3.3), có nút phát/dừng/đặt lại | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-04 | Sơ đồ quan hệ giữa các loại tứ giác (hình vuông ⊂ chữ nhật, thoi ⊂ bình hành…) có thể nhấn vào từng loại | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-05 | Đánh dấu "đã học xong" từng bài; điều hướng bài trước/sau | M | Sơn | Sơn điều hướng; Vũ ghi COMPLETED qua ProgressWriter (TODO). |
| FR-LRN-06 | Ghi chú cá nhân trên bài học | C | Sơn | Sơn sở hữu ghi chú; User chỉ là tham chiếu. |
| FR-LRN-07 | Tìm kiếm bài học và thuật ngữ | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-01 | Bảng vẽ tương tác: tạo điểm, đoạn thẳng, đường thẳng, đường tròn | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-02 | Tạo nhanh các loại tứ giác (hình thang, thang cân, bình hành, chữ nhật, thoi, vuông, nội tiếp) với ràng buộc hình học đúng | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-03 | Kéo thả đỉnh; hình giữ đúng tính chất (ví dụ kéo đỉnh hình bình hành thì cạnh đối vẫn song song) | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-04 | Hiển thị số đo: độ dài cạnh, góc, đường chéo, chu vi, diện tích; cập nhật theo thời gian thực | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-05 | Công cụ: trung điểm, đường vuông góc, đường song song, phân giác, giao điểm | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-06 | Bật/tắt hiển thị tính chất (hai đường chéo, góc bằng nhau, cạnh bằng nhau bằng ký hiệu) | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-07 | Hoàn tác / làm lại (Undo/Redo), xóa, đặt lại bảng | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-08 | Bài thực hành có hướng dẫn: đề yêu cầu "kéo hình để quan sát…", hệ thống kiểm tra kết quả | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-09 | Lưu và tải lại hình vẽ của HS; xuất ảnh PNG | C | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-10 | Hỗ trợ cảm ứng (kéo, phóng to/thu nhỏ) trên thiết bị di động | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-01 | Hiển thị danh sách bài trắc nghiệm theo cấp độ lớp, chủ đề và mức độ (Nhận biết, Thông hiểu, Vận dụng) | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-02 | Câu hỏi 1 đáp án đúng; hỗ trợ nhiều đáp án và đúng/sai; có thể kèm hình minh họa | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-03 | Chế độ luyện tập: chấm từng câu, hiển thị giải thích ngay | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-04 | Chế độ kiểm tra: tính giờ, chấm cuối bài, không xem đáp án giữa chừng | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-05 | Chấm điểm tự động theo thang 10; hiển thị đúng/sai từng câu và giải thích | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-06 | Trộn thứ tự câu hỏi và đáp án | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-07 | Lưu nháp, cho phép tiếp tục bài đang làm dở | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-08 | Làm lại bài; lưu mọi lần làm | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-09 | Nút "Hỏi AI" ngay tại câu hỏi để giải thích sâu hơn | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-01 | Hiển thị đề tự luận kèm hình vẽ, giả thiết, kết luận | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-02 | Gợi ý lời giải theo từng bước, mở dần theo yêu cầu của HS (Gợi ý 1 → 2 → 3 → Lời giải đầy đủ) | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-03 | Mỗi bước gợi ý có thể gắn minh họa trên hình động (vẽ thêm đường phụ, tô góc bằng nhau) | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-04 | HS nhập bài làm (văn bản, công thức) và tự đối chiếu với lời giải mẫu | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-05 | HS tự đánh giá mức độ hiểu (Đã hiểu / Cần xem lại) | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-06 | Ghi nhận số gợi ý đã dùng để phục vụ thống kê điểm yếu | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-07 | Độ khó theo cấp độ: lớp 6 dùng bài toán thực tế/tính toán đơn giản; bài chứng minh bắt đầu từ lớp 7–8 và tăng dần | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-01 | Khung chat hỏi đáp bằng tiếng Việt hoặc tiếng Anh theo ngôn ngữ người dùng | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-02 | Chatbot giải thích lời giải bài tập, khái niệm, tính chất tứ giác ở mức phù hợp với lớp của HS (lớp 6: ngôn ngữ trực quan, ví dụ đời thường; lớp 8–9: thuật ngữ và lập luận chứng minh) | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-03 | Chatbot nhận ngữ cảnh: bài học hoặc câu hỏi HS đang xem để trả lời đúng trọng tâm | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-04 | Giới hạn phạm vi: từ chối lịch sự câu hỏi ngoài chủ đề; không trả lời nội dung không phù hợp lứa tuổi | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-05 | Công thức toán hiển thị đúng định dạng trong câu trả lời | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-06 | Lưu lịch sử hội thoại theo từng phiên; HS có thể xóa | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-07 | HS đánh giá câu trả lời (hữu ích / không hữu ích) và báo lỗi | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-08 | Giới hạn số lượt hỏi mỗi HS mỗi ngày (cấu hình được); hiển thị số lượt còn lại | M | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-09 | Ưu tiên dẫn nguồn là nội dung trong hệ thống (liên kết về bài lý thuyết liên quan); nên dùng kiến trúc truy xuất nội dung (RAG) | S | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-10 | Chatbot ưu tiên dẫn dắt HS tự suy nghĩ (gợi mở) thay vì chỉ đưa đáp án khi HS đang làm bài kiểm tra | C | Đạt | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-01 | Trang tổng quan: % hoàn thành theo cấp độ, chương và chủ đề | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-02 | Lịch sử làm bài: ngày giờ, bài, điểm, thời gian; xem lại bài và đáp án đã chọn | M | Vũ | Đạt sở hữu Attempt/Answer; Vũ hiển thị qua AssessmentReader. |
| FR-PG-03 | Biểu đồ điểm theo thời gian | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-04 | Thống kê điểm mạnh/yếu theo chủ đề | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-05 | Tiếp tục học: quay lại đúng bài đang học dở | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-06 | Gợi ý chủ đề nên ôn lại (dựa trên quy tắc đơn giản, ví dụ điểm < 5) | C | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AD-01 | Đăng nhập quản trị với vai trò riêng, bảo vệ nâng cao | M | Vũ | Vũ AUTH/RBAC; từng page admin phải kiểm tra quyền. |
| FR-AD-02 | Import hàng loạt từ Excel (.xlsx) và JSON: chủ đề, bài lý thuyết, câu trắc nghiệm, đề tự luận, bước gợi ý, kèm nhãn lớp, mức nhận thức và kiến thức tiên quyết | M | Sơn | Sơn điều phối; Đạt validate/ghi Question, Option, Essay, Hint. |
| FR-AD-03 | Kiểm tra dữ liệu trước khi nhập (validate): báo lỗi theo dòng/ô, không nhập nếu lỗi nghiêm trọng | M | Sơn | Mỗi domain validate phần mình; Sơn tổng hợp báo cáo. |
| FR-AD-04 | Tải file mẫu import cho từng loại nội dung | M | Sơn | Sơn mẫu lesson; Đạt mẫu question/essay. |
| FR-AD-05 | Xem trước nội dung sau import; trạng thái Nháp / Đã xuất bản | M | Sơn | Sơn lesson; Đạt question/essay, không ghi chéo. |
| FR-AD-06 | Xuất bản, gỡ bản, sửa từng mục nội dung và lưu phiên bản | S | Sơn | Version thuộc owner từng loại nội dung. |
| FR-AD-07 | Quản lý hình động: nhập cấu hình hình (JSON mô tả hình học) kèm bài học | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AD-08 | Nhật ký import (người thực hiện, thời gian, số bản ghi thành công/lỗi) | S | Sơn | Sơn sở hữu ImportLog; domain khác báo kết quả qua contract TODO. |
| FR-AD-09 | Quản lý người dùng: tìm kiếm, khóa/mở khóa tài khoản | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AD-10 | Thống kê: số HS, lượt học, bài làm nhiều/ít, câu hỏi AI thường gặp, đánh giá chatbot | S | Vũ | Vũ dashboard tổng hợp; đọc ContentReader/AssessmentReader. |
| FR-AD-11 | Cấu hình hệ thống: hạn mức hỏi AI, thời gian phiên | S | Đạt | Đạt quota AI; Vũ thời hạn session (hai cấu hình khác nhau). |
| FR-I18-01 | Chuyển đổi Việt/Anh ở mọi màn hình; ghi nhớ lựa chọn theo tài khoản | M | Sơn | Sơn bộ dịch UI; Vũ ghi User.language; mỗi owner dịch page mình. |
| FR-I18-02 | Nội dung học có trường song ngữ (vi, en); nếu thiếu bản Anh thì hiển thị bản Việt kèm thông báo | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-I18-03 | Định dạng ngày, số theo ngôn ngữ | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-01 | Khi đăng ký, HS chọn lớp (6, 7, 8, 9); lớp này là cấp độ khởi đầu | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-02 | HS đổi cấp độ trong hồ sơ; tiến độ của từng cấp độ được lưu riêng | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-03 | Lộ trình hiển thị theo cấp độ; mỗi chủ đề/bài/câu hỏi gắn nhãn lớp và mức nhận thức | M | Vũ | Vũ hiển thị lộ trình; Sơn metadata; Đạt metadata câu hỏi. |
| FR-LV-04 | Cùng một loại tứ giác hiển thị nội dung khác nhau theo cấp độ (lớp 6: mô tả trực quan; lớp 7–8: tính chất; lớp 8–9: chứng minh) | M | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-05 | HS truy cập tự do nội dung cấp thấp hơn để ôn tập | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-06 | Mở khóa cấp cao hơn khi hoàn thành ≥ 70% bài học và điểm trung bình ≥ 6/10 (ngưỡng cấu hình được); HS có thể chọn "học vượt" kèm cảnh báo | S | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-07 | Mỗi bài hiển thị kiến thức tiên quyết (liên kết về bài nền ở cấp dưới) | S | Vũ | Vũ hiển thị/gợi ý; Sơn ghi REQUIRES. |
| FR-LV-08 | Khi điểm một chủ đề < 5/10, gợi ý ôn các bài tiên quyết ở cấp thấp hơn | S | Vũ | Vũ gợi ý; Đạt cung cấp điểm; Sơn cung cấp tiên quyết. |
| FR-LV-09 | Bộ công cụ hình học động thích ứng theo cấp độ (lớp 6 rút gọn, các cấp cao mở thêm công cụ) | S | Sơn | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-10 | Dashboard hiển thị tiến độ riêng cho từng cấp độ | M | Vũ | TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-11 | Bài kiểm tra xếp loại đầu vào để gợi ý cấp độ phù hợp | C | Vũ | Vũ chọn lớp gợi ý; Đạt đề/chấm bài đầu vào (TODO Could). |

## Use case và màn hình

| Use case | Owner | Màn hình | Skeleton |
|---|---|---|---|
| UC-01 quiz | Đạt | SCR-07/08 | Chỉ đọc lịch sử seed; chưa submit, draft hay sync offline |
| UC-02 AI | Đạt | SCR-10 | Mock contract, context graph; chưa quota, LLM, filtering, timeout/refund |
| UC-03 import | Sơn điều phối, Đạt phần assessment | SCR-14/15 | Mẫu JSON/CSV; chưa upload, preview hay ghi import |
| UC-04 geometry | Sơn | SCR-05/06 | Slider hình chữ nhật; chưa kéo thả hay bảo vệ điểm suy biến |
| UC-05 levels | Vũ | SCR-03/04/17 | Đọc lớp/lộ trình; chưa unlock hay cập nhật progress |

SCR-01: core/Home; SCR-02/03/04/11/12/16/17: Vũ; SCR-05/06/14/15: Sơn; SCR-07/08/09/10: Đạt. SCR-13: Vũ điều phối dashboard, hai domain cung cấp thống kê. SCR-14/15: mỗi loại nội dung do owner tương ứng ghi.

## Quy tắc cần giữ

- AUTH: email duy nhất, mật khẩu ≥8 ký tự có chữ/số; xác thực email mới lưu progress; guardian consent dưới 16 tuổi; không bỏ qua các điều kiện này khi làm AUTH thật. Demo chỉ dùng danh tính giả và dữ liệu seed.
- LV: chọn lớp 6–9; xem lại lớp dưới; lưu riêng từng lớp; ngưỡng giả định 70% và 6/10 có thể cấu hình, học vượt phải cảnh báo/xác nhận. Chưa chốt Q4 nên không bật khóa thật.
- Nội dung: lớp, mức nhận thức, thứ tự, trạng thái; bản Việt bắt buộc; Anh tùy chọn có fallback thông báo; không dùng AI tự sinh đề.
- Import: topic_code tồn tại; tiên quyết tồn tại và grade thấp hơn hoặc bằng; correct nằm trong options; lỗi nghiêm trọng không ghi; mặc định Nháp. Cần thêm kiểm tra không chu trình REQUIRES.
- Geometry: giữ ràng buộc khi kéo, chặn suy biến, công cụ theo lớp; slider demo không đáp ứng UC-04 đầy đủ.
- Quiz: thang 10, mọi lần làm và từng lựa chọn phải lưu; không chia sẻ đáp án với client trước thời điểm được phép ở kiểm tra thật.
- AI: theo lớp/ngôn ngữ/ngữ cảnh, giới hạn chủ đề/lứa tuổi, quota theo ngày; lỗi/quá 30s không trừ lượt. Mock không thực hiện những đảm bảo này.

## NFR và phạm vi

E10 do cả nhóm review, người tích hợp skeleton điều phối. UX-01…04, PERF-01…05, SEC-01…06, REL-01…05 và COMP đều **TODO/chưa nghiệm thu sản phẩm**. Có tham số Cypher, secrets ngoài Git và test nền, nhưng chưa chứng nhận WCAG, tải 500 user, 30fps, chất lượng AI, pháp lý, HTTPS, backup hay SLA. PB-39/40 và DoD staging/UAT được hoãn; tiêu chí skeleton riêng ở VERIFICATION.md. Native app/offline, vai trò giáo viên/phụ huynh, thanh toán, gamification, ảnh OCR và chương khác giữ ngoài phạm vi. Guardian consent không đồng nghĩa vai trò phụ huynh.
