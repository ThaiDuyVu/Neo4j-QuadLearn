# Git/GitHub cho nhóm 3 người

Repo nhóm: `git@github.com:ThaiDuyVu/Neo4j-QuadLearn.git`. Người tích hợp commit skeleton ổn định và đưa lên main trước; cả nhóm dùng cùng GitHub repo, DB riêng local. Không GitFlow/hook bắt buộc.

## Khởi tạo main (người tích hợp)

Nếu root chưa có Git:

```
git init -b main
git status
git add .
git diff --cached --stat
git commit -m "chore: initialize QuadLearn Neo4j skeleton"
git remote add origin <URL_REPO_GITHUB_CUA_NHOM>
git push -u origin main
```

Trước commit, kiểm tra `.env`, venv, log và thông tin nhạy cảm được ignore; `git check-ignore .env`. Nếu repo đã có main thì dùng repo hiện tại, không init hay đè lịch sử. Không dùng secret thật trong tests/docs/Cypher/ảnh chụp. Commit `.env.example` với password rỗng.

## Bắt đầu mỗi người

```
git clone <URL_REPO_GITHUB_CUA_NHOM>
cd QuadLearn
git switch main
git pull --ff-only origin main
```

Mỗi người chạy **một** lệnh tương ứng trên clone của mình:

```
git switch -c feature/vu-identity-learning-path
git switch -c feature/son-learning-geometry
git switch -c feature/dat-assessment-ai
```

Không cần chạy cả ba trong một clone. Làm trong feature mình, test domain; shared changes thông báo cả nhóm và review trước merge.

## Commit → PR → merge

```
git status
git add app/features/<domain>/
git diff --cached
git commit -m "feat(<domain>): add focused functionality"
git push -u origin <branch-cua-minh>
```

GitHub → Compare & pull request → base main, head branch cá nhân. Mô tả vấn đề, FR, thay đổi, test, ảnh demo và shared files/schema thay đổi; đánh dấu TODO còn lại. Ít nhất một thành viên review. Sau checks/test, merge từng PR (merge commit hoặc squash thống nhất với nhóm). Không merge đồng thời hai PR chưa cập nhật shared contract tương thích. Không force push main.

## Lấy thay đổi main / PR conflict

Commit hoặc stash việc đang làm trước; không merge khi working tree bừa bộn:

```
git fetch origin
git switch <branch-cua-minh>
git merge origin/main
```

Nếu conflict, `git status` liệt kê file; mở local editor, đọc cả hai phía, bỏ `<<<<<<<`, `=======`, `>>>>>>>`, giữ logic đúng và contract tương thích. Trao đổi owner nếu file shared/feature người khác. **Có thể giải quyết bằng Git CLI local, không bắt buộc GitHub UI.**

```
git add <file-da-giai-quyet>
git commit -m "merge: resolve conflicts with main"
python -m pytest -m "not integration"
git push
```

Muốn hủy merge đang dang dở: `git merge --abort`. Không dùng `git reset --hard` để “sửa conflict” khi chưa giữ việc của mình. Sau push PR tự cập nhật; review lại file thay đổi. Rebase không bắt buộc, quy trình chung dùng merge để tránh force push.

Sau PR đã merge:

```
git switch main
git pull --ff-only origin main
```

Nếu tiếp tục branch cá nhân còn tồn tại, switch về branch, `git merge origin/main`; hoặc tạo branch tác vụ mới từ main. Không viết trực tiếp main. Nếu đã lỡ commit secret, báo nhóm, thay/thu hồi secret và xử lý lịch sử có phối hợp; chỉ xóa file ở commit mới không xóa secret lịch sử.

Không commit `.env`, `.venv`, password/API key, graph DB local, cache/log, data trẻ em thật hay Docker volumes. Feature workflows dùng cùng quy trình này. Trước PR: kiểm tra import, test, FR mapping và ownership; DB fixture shared sửa cần báo cả nhóm.
