# Câu hỏi mở

Đồ án và Neo4j local đã được người dùng chốt; các đề xuất thương mại trong SRS không được triển khai mặc định. Chưa chốt những điểm dưới đây:

| Điểm | Nguồn | Owner cần chốt | Tạm thời trong skeleton |
|---|---|---|---|
| Bộ SGK và phân bổ kiến thức theo lớp? | Q1, §2.2 | Sơn/cả nhóm | Nội dung demo có nhãn, chưa thẩm định |
| Quy mô/UAT, có thương mại hóa tương lai? | Q2, NFR | cả nhóm | Đồ án local; không cam kết 500 users/SLA |
| Nhà cung cấp LLM/ngân sách? | Q3 | Đạt | Mock, không API key |
| Ngưỡng unlock, học vượt có tự do, thứ tự soạn lớp? | Q4/A7 | Vũ + Sơn | 70% và 6/10 là giả định SRS; chưa enforce |
| Ai soạn, dịch Anh và giáo viên nào thẩm định? | §11.5/8 | Sơn/cả nhóm | Mẫu Việt và tiêu đề Anh, chưa dịch đầy đủ |
| Có vai trò giáo viên/phụ huynh phiên bản sau? | §11.4 | cả nhóm | Ngoài phạm vi; consent vẫn yêu cầu nghiệp vụ |
| Tên miền/nhận diện? | §11.6 | cả nhóm | Streamlit local, không deploy |
| Guardian consent qua email có đủ, xác định tuổi thế nào? | AUTH-12/§11.9 | Vũ | Không tài khoản trẻ em thật; chưa tích hợp email |
| Trung bình điểm lấy mọi lần/latest/best? Topic→Level tính thế nào? | PG/LV không xác nhận | Vũ + Đạt | Không tính unlock, seed projection chỉ minh họa |
| Hoàn thành bài bằng thao tác nào? Essay hiểu/gợi ý tính progress ra sao? | LRN-05/ES/PG | Vũ + Sơn + Đạt | Cạnh seed không cập nhật từ UI |
| Hình thang “ít nhất một” hay “đúng một” cặp song song? | SGK/Q1 | Sơn | Chưa nối bình hành IS_A hình thang |
| Quiz là collection riêng hay theo topic? Placement scoring? | QZ/LV-11, dữ liệu §4 | Đạt + Vũ | Một Attempt FOR_TOPIC; chưa node Quiz |
| Offline sync trong UC-01 mâu thuẫn offline ngoài phạm vi? | UC-01/§1.4 | cả nhóm | Chưa draft/offline sync |
| Import atomic toàn batch hay cho từng loại? Versioning và prerequisite sửa/xóa? | UC-03/AD | Sơn + Đạt | Mẫu schema; không import write |
| Ngày quota AI theo Asia/Ho_Chi_Minh? Lượt từ chối phạm vi có tính không? | AI-08/UC-02 | Đạt | Chưa quota; lỗi >30s không trừ theo SRS |
| Thư viện geometry/giấy phép và embed có mobile 30fps? | GEO/R3/R6 | Sơn | Slider/SVG không đạt canvas đầy đủ |

Khi chốt: cập nhật tài liệu, contract/schema liên quan và test rồi mở PR shared. Không xem quyết định tạm thời là sửa nghiệp vụ đã được phê duyệt. Chính sách dữ liệu trẻ em và yêu cầu pháp lý sản phẩm cần đánh giá khi mở rộng, skeleton chưa là xác nhận tuân thủ.

## Quyết định tạm thời khi phát triển Vũ

- Unlock dùng 70% và 6/10 theo A7, cấu hình qua VU_UNLOCK_COMPLETION/VU_UNLOCK_SCORE; Q4 vẫn chưa được duyệt, không ghi là yêu cầu mới đã chốt.
- Average mặc định `all`, có `latest` theo thứ tự newest-first của AssessmentReader; điểm chỉ từ completed của topic có published lessons trong level. VU_AVERAGE_POLICY có thể đổi.
- Tuổi do người dùng khai báo, guardian token dev không xác minh phụ huynh thực tế. Verify/guardian token local TTL 24 giờ là chọn triển khai tạm thời, reset TTL 30 phút giữ SRS.
- Auth session idle backend 7 ngày, raw token trong Streamlit state; remember-me/cookie persistence chưa triển khai.
- Hoàn thành bằng nút xác nhận tại lộ trình; không suy ra tự luận/geometry completion chưa chốt.
- Timestamps/detail answers, placement và contract xóa dữ liệu cá nhân vẫn thiếu ở Đạt; không truy vấn repository nội bộ domain Đạt để bỏ qua contract.
