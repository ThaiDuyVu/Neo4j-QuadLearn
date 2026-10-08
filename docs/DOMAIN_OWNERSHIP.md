# Quyền sở hữu domain

| Domain | Người | Chức năng / FR | Folder | Node / cạnh ghi | Contract / dependency |
|---|---|---|---|---|---|
| identity_learning_path | Vũ | AUTH-01…12, PG-01…06, LV-01/02/03/05/06/07/08/10/11; AD-01/09/10 | app/features/identity_learning_path/ | User, Progress; STUDIES_AT, LEARNING, COMPLETED, HAS_PROGRESS, FOR_LEVEL | cung cấp IdentityReader; đọc ContentReader/AssessmentReader |
| learning_geometry | Sơn | LRN-01…07, GEO-01…10, I18-01…03; LV-04/09; AD-02…08 | app/features/learning_geometry/ | Level/catalog, Chapter, Topic, Lesson, shape/config, ImportLog; HAS_CHAPTER/TOPIC/LESSON, REQUIRES, RELATED_TO, IS_A, ABOUT, ILLUSTRATED_BY | cung cấp ContentReader; đọc IdentityReader; ProgressWriter TODO |
| assessment_ai | Đạt | QZ-01…09, ES-01…07, AI-01…10; AD-11 quota; chi tiết PG-02, import assessment AD-02…06 | app/features/assessment_ai/ | Question/Option, Essay/Hint, Attempt/Answer, Chat; HAS_QUESTION/OPTION/ESSAY/HINT, ATTEMPTED, FOR_TOPIC, HAS_ANSWER, ANSWERS, SELECTED, HAS_CHAT/MESSAGE, CONTEXT_LESSON | cung cấp AssessmentReader; đọc IdentityReader/ContentReader |

FR đầy đủ và trách nhiệm phối hợp: SRS_TRACEABILITY.md. Bảng trên dùng prefix rút gọn, không đổi mã SRS. Shared contracts/core/database/docs schema: vùng review chung, người làm skeleton điều phối ban đầu. Seed là fixture chung, không cho domain quyền ghi chéo runtime.

**Level do Sơn quản lý catalog 6–9**, Vũ chỉ chọn/đổi liên kết User→Level. **Tiên quyết do Sơn ghi**, Vũ đọc để unlock/gợi ý. **Chi tiết Attempt do Đạt ghi**, Vũ tính/ghi Progress theo kết quả. LRN-05 UI của Sơn yêu cầu Vũ ghi COMPLETED qua contract TODO. AD-11 tách quota AI của Đạt và timeout session của Vũ. I18 UI do Sơn định nghĩa từ điển, mỗi owner dịch page mình, Vũ ghi preference user.

Không import repository/service feature khác. `core/bootstrap.py` nối implementation qua ports là ngoại lệ tích hợp được quy định, không circular imports. Một domain có thể tạo cạnh tham chiếu User/Topic theo bảng schema, nhưng không sửa node thuộc owner khác. Xóa user cần quy trình phối hợp để Đạt xóa history rồi Vũ xóa identity, không tự DETACH DELETE toàn dữ liệu domain khác. Chưa triển khai xóa tài khoản.
