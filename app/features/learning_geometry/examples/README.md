# Mẫu import (TODO importer)

`lesson.json` theo §4.2 SRS; prerequisites dùng ID lesson chuẩn thay mã hiển thị, cần nhóm chốt converter legacy code. topic_code PARALLELOGRAM lớp 8 và prerequisite lesson:7:parallel có trong seed. Chưa có lesson ID trong payload SRS: importer cần gán UUID/ID ổn định trước ghi và không tự ghi đè bài published demo.

`questions_template.csv` là **header/schema chuẩn bị cho Excel**, không giả là file .xlsx hoặc importer đã chạy. Có thể mở CSV trong Excel rồi Save As .xlsx; khi Đạt triển khai parser sẽ thêm dependency Excel có lý do. Giữ header theo SRS: `level` là difficulty, `grade` là lớp. correct theo letter A…D, phải validate tập options. Đạt sở hữu validate/ghi question. Mẫu chỉ minh họa, không chạy tự động.

Bắt buộc bản Việt; Anh optional fallback; grade 6–9; topic_code+grade tồn tại; prerequisites grade ≤ source; validate toàn batch, không chu trình, preview lỗi dòng/ô; lưu Nháp, chưa xuất bản. Hình config renderer JSON có thể thành GeometryConfig property config_json, quan hệ bài/tiên quyết không nhét JSON.
