# Product Backlog theo SRS

56 story giữ ưu tiên và tiêu chí SRS. Sprint/SP là ước lượng BA của sản phẩm, không kế hoạch skeleton. Tất cả còn TODO ở mức story đầy đủ; PB-01 chỉ hoàn thành khung local, không CI/CD hay staging.

| ID | Epic | Story | Tiêu chí SRS | M/S/C | SP | Sprint SRS | Owner |
|---|---|---|---|---|---|---|---|
| PB-01 | E10 | Là đội dự án, tôi muốn thiết lập hạ tầng, CI/CD, khung dự án | Có môi trường dev/staging, pipeline chạy được | M | 5 | 1 | Shared / cả nhóm; staging, CI/CD, production ngoài skeleton |
| PB-02 | E1 | Là HS, tôi muốn đăng ký bằng email + mật khẩu để có tài khoản | Validate đúng FR-AUTH-02; email trùng báo lỗi; gửi email xác thực | M | 5 | 1 | Vũ |
| PB-03 | E1 | Là HS, tôi muốn đăng nhập/đăng xuất | Đăng nhập đúng vào dashboard; sai báo lỗi chung; khóa sau 5 lần sai | M | 3 | 1 | Vũ |
| PB-04 | E1 | Là HS, tôi muốn đăng nhập bằng Google | Lần đầu tự tạo tài khoản; email trùng thì liên kết | M | 3 | 1 | Vũ |
| PB-05 | E1 | Là HS, tôi muốn quên/đổi mật khẩu qua email | Link hết hạn 30 phút, dùng một lần | M | 5 | 2 | Vũ |
| PB-06 | E9 | Là người dùng, tôi muốn chuyển Việt/Anh | Toàn bộ giao diện đổi ngôn ngữ; lưu lựa chọn | M | 5 | 2 | Sơn (Vũ ghi ngôn ngữ tài khoản) |
| PB-07 | E2 | Là Admin, tôi muốn đăng nhập trang quản trị | Chỉ vai trò admin vào được | M | 3 | 2 | Sơn |
| PB-08 | E2 | Là Admin, tôi muốn import chủ đề và bài lý thuyết từ Excel/JSON | Validate, báo lỗi theo dòng, lưu Nháp | M | 8 | 2 | Sơn |
| PB-09 | E2 | Là Admin, tôi muốn import câu trắc nghiệm hàng loạt | Như PB-08; đúng cấu trúc đáp án | M | 8 | 2 | Đạt (Sơn điều phối import) |
| PB-10 | E2 | Là Admin, tôi muốn tải file mẫu và xem trước, xuất bản nội dung | File mẫu đúng cấu trúc; xuất bản/gỡ bản được | M | 5 | 3 | Sơn |
| PB-11 | E3 | Là HS, tôi muốn xem lộ trình chương – chủ đề | Hiển thị đúng theo cấu trúc, trạng thái đã học | M | 5 | 3 | Sơn |
| PB-12 | E3 | Là HS, tôi muốn đọc bài lý thuyết có công thức | Công thức hiển thị đúng trên mobile/desktop | M | 5 | 3 | Sơn |
| PB-13 | E4 | Là HS, tôi muốn xem hình động minh họa trong bài | Phát/dừng/đặt lại; chạy mượt ≥ 30 fps | M | 8 | 3 | Sơn |
| PB-14 | E4 | Là HS, tôi muốn dựng và kéo thả từng loại tứ giác | Giữ đúng ràng buộc hình học cho 7 loại tứ giác | M | 13 | 3–4 | Sơn |
| PB-15 | E4 | Là HS, tôi muốn xem số đo (cạnh, góc, chéo, chu vi, diện tích) theo thời gian thực | Số đo cập nhật khi kéo | M | 5 | 4 | Sơn |
| PB-16 | E4 | Là HS, tôi muốn hoàn tác/làm lại và dùng được trên cảm ứng | Undo/Redo; kéo bằng ngón tay | M | 5 | 4 | Sơn |
| PB-17 | E4 | Là HS, tôi muốn dùng công cụ vẽ (trung điểm, vuông góc, song song, phân giác) | Công cụ hoạt động đúng | S | 8 | 5 | Sơn |
| PB-18 | E4 | Là HS, tôi muốn bật/tắt hiển thị tính chất của hình | Ký hiệu cạnh/góc bằng nhau hiển thị đúng | S | 5 | 5 | Sơn |
| PB-19 | E5 | Là HS, tôi muốn làm trắc nghiệm chế độ luyện tập | Chấm từng câu, có giải thích | M | 8 | 4 | Đạt |
| PB-20 | E5 | Là HS, tôi muốn xem điểm và đáp án chi tiết sau khi làm | Điểm thang 10; hiển thị đúng/sai từng câu | M | 5 | 4 | Đạt |
| PB-21 | E8 | Là HS, tôi muốn lưu lịch sử làm bài và xem lại | Mọi lần làm được lưu; xem lại đáp án đã chọn | M | 5 | 5 | Đạt ghi / Vũ đọc |
| PB-22 | E8 | Là HS, tôi muốn xem tiến độ tổng quan và "tiếp tục học" | % hoàn thành đúng; quay lại đúng bài dở | M | 5 | 5 | Vũ |
| PB-23 | E6 | Là HS, tôi muốn xem đề tự luận kèm hình | Hiển thị giả thiết, kết luận, hình | M | 5 | 5 | Đạt |
| PB-24 | E6 | Là HS, tôi muốn mở gợi ý từng bước và lời giải đầy đủ | Gợi ý mở dần theo từng lần bấm | M | 8 | 5 | Đạt |
| PB-25 | E2 | Là Admin, tôi muốn import đề tự luận, các bước gợi ý | Validate; liên kết bước với đề | M | 8 | 5 | Đạt (Sơn điều phối import) |
| PB-26 | E7 | Là HS, tôi muốn hỏi chatbot AI và nhận giải thích | Trả lời đúng ngữ cảnh, có công thức, ≤ 30 giây | M | 13 | 6 | Đạt |
| PB-27 | E7 | Là hệ thống, tôi cần giới hạn phạm vi và lọc nội dung chatbot | Từ chối ngoài phạm vi; lọc nội dung không phù hợp | M | 8 | 6 | Đạt |
| PB-28 | E7 | Là hệ thống, tôi cần giới hạn lượt hỏi AI mỗi ngày | Hiển thị lượt còn lại; chặn khi hết | M | 3 | 6 | Đạt |
| PB-29 | E7 | Là HS, tôi muốn nút "Hỏi AI" ở bài học/câu hỏi để truyền ngữ cảnh | Chatbot nhận đúng nội dung đang xem | S | 5 | 7 | Đạt |
| PB-30 | E7 | Là HS, tôi muốn đánh giá câu trả lời và xóa lịch sử chat | Lưu đánh giá; xóa được phiên chat | S | 3 | 7 | Đạt |
| PB-31 | E7 | Là hệ thống, tôi muốn chatbot dùng RAG trên nội dung đã import | Câu trả lời dẫn liên kết bài liên quan | S | 8 | 7 | Đạt |
| PB-32 | E5 | Là HS, tôi muốn làm bài kiểm tra tính giờ, trộn câu, lưu nháp | Tính giờ đúng; tiếp tục được bài dở | S | 8 | 7 | Đạt |
| PB-33 | E3 | Là HS, tôi muốn xem sơ đồ quan hệ giữa các loại tứ giác | Nhấn vào nút để mở bài tương ứng | S | 5 | 7 | Sơn |
| PB-34 | E8 | Là HS, tôi muốn xem biểu đồ điểm và điểm mạnh/yếu | Biểu đồ đúng dữ liệu | S | 5 | 8 | Vũ |
| PB-35 | E4 | Là HS, tôi muốn làm bài thực hành hình động có kiểm tra kết quả | Hệ thống xác nhận khi hoàn thành yêu cầu | S | 8 | 8 | Sơn |
| PB-36 | E1 | Là HS, tôi muốn sửa hồ sơ, xóa tài khoản | Xóa dữ liệu theo yêu cầu | S | 5 | 8 | Vũ |
| PB-37 | E2 | Là Admin, tôi muốn quản lý người dùng, xem thống kê và nhật ký import | Khóa/mở khóa; thống kê đúng | S | 8 | 8 | Sơn |
| PB-38 | E3 | Là HS, tôi muốn tìm kiếm bài học | Tìm theo từ khóa trả kết quả liên quan | S | 3 | 8 | Sơn |
| PB-39 | E10 | Là đội dự án, tôi cần kiểm thử hiệu năng, bảo mật, kiểm thử chất lượng AI | Đạt NFR-PERF, NFR-SEC, NFR-REL-05 | M | 13 | 9 | Shared / cả nhóm; staging, CI/CD, production ngoài skeleton |
| PB-40 | E10 | Là đội dự án, tôi cần UAT, sửa lỗi và phát hành | Biên bản UAT được duyệt; triển khai production | M | 8 | 10 | Shared / cả nhóm; staging, CI/CD, production ngoài skeleton |
| PB-41 | E3 | Là HS, tôi muốn ghi chú cá nhân trong bài | Lưu và hiển thị ghi chú | C | 3 | Sau MVP | Sơn |
| PB-42 | E4 | Là HS, tôi muốn lưu/tải hình vẽ và xuất ảnh PNG | Lưu được nhiều hình; xuất PNG | C | 5 | Sau MVP | Sơn |
| PB-43 | E8 | Là HS, tôi muốn được gợi ý chủ đề cần ôn lại | Gợi ý theo quy tắc điểm | C | 5 | Sau MVP | Vũ |
| PB-44 | E7 | Là HS, tôi muốn chatbot dẫn dắt gợi mở khi đang kiểm tra | Không đưa đáp án trực tiếp ở chế độ kiểm tra | C | 5 | Sau MVP | Đạt |
| PB-45 | E11 | Là HS, tôi muốn chọn lớp (6–9) khi đăng ký để vào đúng cấp độ | Bắt buộc chọn lớp; vào đúng lộ trình của lớp | M | 3 | 2 | Vũ |
| PB-46 | E11 | Là HS, tôi muốn xem lộ trình theo cấp độ, nội dung gắn nhãn lớp và mức nhận thức | Hiển thị đúng nhãn; lọc được theo lớp | M | 5 | 3 | Vũ |
| PB-47 | E11 | Là HS, tôi muốn cùng một loại tứ giác hiển thị nội dung phù hợp từng lớp (trực quan → tính chất → chứng minh) | Nội dung và thuật ngữ đúng lớp | M | 8 | 4 | Sơn |
| PB-48 | E11 | Là HS, tôi muốn xem tự do nội dung cấp thấp hơn để ôn | Không bị chặn; tiến độ lưu riêng từng cấp | M | 3 | 4 | Vũ |
| PB-49 | E11 | Là HS, tôi muốn mở khóa cấp cao hơn khi đủ điều kiện hoặc chọn học vượt | Ngưỡng cấu hình được; cảnh báo khi học vượt | S | 5 | 6 | Vũ |
| PB-50 | E11 | Là HS, tôi muốn thấy kiến thức tiên quyết và gợi ý ôn khi làm sai nhiều | Liên kết đúng bài nền; gợi ý khi điểm < 5 | S | 8 | 7 | Vũ (Đạt cung cấp điểm/đề; Sơn tiên quyết) |
| PB-51 | E11 | Là HS, tôi muốn công cụ hình động thích ứng theo lớp (lớp 6 đơn giản) | Bộ công cụ đúng từng cấp; lớp 6 không bị rối | S | 5 | 6 | Sơn |
| PB-52 | E7 | Là HS, tôi muốn chatbot trả lời phù hợp với lớp của tôi | Cùng câu hỏi, lớp 6 và lớp 8 nhận cách giải thích khác nhau; có bộ kiểm thử theo lớp | M | 5 | 6 | Đạt |
| PB-53 | E2 | Là Admin, tôi muốn import kèm lớp, mức nhận thức, kiến thức tiên quyết | Validate lớp ∈ 6–9; tiên quyết tồn tại | M | 5 | 3 | Sơn |
| PB-54 | E1 | Là hệ thống, tôi cần xác nhận của phụ huynh với HS dưới 16 tuổi | Gửi email xác nhận; chỉ kích hoạt sau khi đồng ý | M | 5 | 3 | Vũ |
| PB-55 | E8 | Là HS, tôi muốn xem tiến độ riêng theo từng cấp độ | Dashboard hiển thị % mỗi lớp | M | 3 | 5 | Vũ |
| PB-56 | E11 | Là HS, tôi muốn làm bài kiểm tra xếp loại đầu vào | Hệ thống gợi ý cấp độ phù hợp | C | 8 | Sau MVP | Vũ (Đạt cung cấp điểm/đề; Sơn tiên quyết) |

Thứ tự đề nghị cho nhóm: ổn định contracts/schema → lớp 8 lõi và AUTH demo-to-real → quiz + progress → JSON import → geometry spike → AI mock/context/quota → Should/Could sau khi Must liên quan đã kiểm thử. Nội dung lớp 6/7/9 phải đối chiếu SGK và được thẩm định trước xuất bản.
