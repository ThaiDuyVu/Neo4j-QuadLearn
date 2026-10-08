# Git workflow của Sơn

Tuân thủ `docs/GIT_GITHUB_WORKFLOW.md`; không quy trình riêng khác nhóm. Folder chính: `app/features/learning_geometry/`. Branch: `feature/son-learning-geometry`.

Sau khi skeleton ổn định đã lên main:

```
git switch main
git pull --ff-only origin main
git switch -c feature/son-learning-geometry
```

Làm việc trong folder mình, test trước commit:

```
python -m pytest app/features/learning_geometry/tests -q
git status
git add app/features/learning_geometry/
git diff --cached
git commit -m "feat(son): add domain functionality"
git push -u origin feature/son-learning-geometry
```

Commit gợi ý: `feat(son): add focused service`, `test(son): cover invalid input`, `docs(son): document domain contract`. Dùng mô tả cụ thể chức năng thật, không “complete all FR” cho placeholder. Không add `.env`/venv/secrets.

GitHub tạo PR base main, head `feature/son-learning-geometry`. Ghi FR liên quan, behavior, test và TODO; nhờ một bạn review, merge sau khi tương thích. Chỉ merge từng PR đã cập nhật main. Lấy thay đổi main trong branch:

```
git fetch origin
git switch feature/son-learning-geometry
git merge origin/main
```

Nếu conflict: `git status`, sửa file local/bỏ conflict markers, xác nhận logic với owner, `git add <file>`, `git commit -m "merge: resolve conflicts with main"`, chạy tests, `git push`. Không bắt buộc giải quyết trên GitHub UI; không force push main. Hủy merge dở: `git merge --abort`. Commit/stash trước merge, không reset hard mất việc.

Sau PR merge: `git switch main`, `git pull --ff-only origin main`; tạo branch tiếp từ main hoặc merge main vào branch còn dùng. Không code trực tiếp main.

**Phải thông báo cả nhóm** khi thay ports/DTO/AppContext/registry convention, schema/seed/constraints, config/dependencies/Compose, cần sửa vùng chung hay nhận thấy dữ liệu/relationship owner khác phải thay. Muốn chỉnh feature bạn khác: gửi đề xuất để owner thực hiện/review, không tự ghi hộ.
