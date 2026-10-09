# DOMAIN OWNER: VU. CORE LEARNING: tính tiến độ, quyền cấp độ và gợi ý ôn tập.
from statistics import mean
from app.shared.models.dto import LevelSummary
from ..models.errors import IdentityError
from ..models.policy import IdentityPolicy


class LearningPathService:
    def __init__(self, repository, identity, content, assessment, catalog, policy=None):
        self.repository = repository
        self.identity = identity
        self.content = content
        self.assessment = assessment
        self.catalog = catalog
        self.policy = policy or IdentityPolicy.load()

    def _user(self, user_id):
        user = self.identity.current_user()
        if not user or user.id != user_id:
            raise IdentityError("Không có quyền đọc tiến độ này.")
        return user

    def levels(self, user_id):
        user = self._user(user_id)
        profile = self.identity.repository.profile(user_id)
        baseline = profile.get("starting_grade", user.grade)
        completed, opened = self.repository.snapshot(user_id)
        highest = max([baseline, user.grade, *opened])
        attempts = [
            a for a in self.assessment.attempts(user_id) if a.status == "completed"
        ]
        if self.policy.average_policy == "latest":
            # Contract trả mới nhất trước; không giả có timestamps ngoài contract.
            latest = {}
            for a in attempts:
                latest.setdefault(a.topic_id, a)
            attempts = list(latest.values())
        result = []
        for grade in (6, 7, 8, 9):
            lessons = self.content.lessons(grade)
            topics = {l.topic_id for l in lessons}
            scores = [
                a.score for a in attempts if a.topic_id in topics and 0 <= a.score <= 10
            ]
            done = sum(l.id in completed for l in lessons)
            result.append(
                LevelSummary(
                    grade,
                    len(lessons),
                    done,
                    100 * done / len(lessons) if lessons else 0,
                    mean(scores) if scores else None,
                    grade <= highest,
                )
            )
        return result

    def access(self, user_id, grade):
        if grade not in (6, 7, 8, 9):
            raise IdentityError("Lớp phải từ 6 đến 9.")
        levels = self.levels(user_id)
        target = levels[grade - 6]
        if target.unlocked:
            return True
        previous = levels[grade - 7] if grade > 6 else None
        return bool(
            previous
            and previous.unlocked
            and previous.total > 0
            and previous.completion >= self.policy.completion_threshold
            and previous.average_score is not None
            and previous.average_score >= self.policy.score_threshold
        )

    def change_level(self, grade, confirm_skip=False):
        user = self.identity.require_user()
        eligible = self.access(user.id, grade)
        if not eligible and not (self.policy.allow_skip and confirm_skip):
            raise IdentityError(
                "Chưa đạt ngưỡng. Muốn học vượt phải đọc cảnh báo và xác nhận."
            )
        self.repository.change_level(
            user.id, grade, "threshold_or_available" if eligible else "confirmed_skip"
        )

    def catalog_for(self, user_id, grade):
        if not self.access(user_id, grade):
            raise IdentityError(
                "Cấp độ đang khóa; chuyển cấp/học vượt trong hồ sơ trước."
            )
        return self.catalog.catalog(grade)

    def _lesson(self, user_id, lesson_id):
        self.identity.require_user(user_id)
        for grade in (6, 7, 8, 9):
            lesson = next(
                (l for l in self.content.lessons(grade) if l.id == lesson_id), None
            )
            if lesson:
                if not self.access(user_id, grade):
                    raise IdentityError("Bài học thuộc cấp độ chưa mở.")
                return lesson
        raise IdentityError("Bài học không tồn tại hoặc chưa xuất bản.")

    def start_lesson(self, user_id, lesson_id):
        self._lesson(user_id, lesson_id)
        self.repository.mark_lesson(user_id, lesson_id, False)

    def complete_lesson(self, user_id, lesson_id):
        self._lesson(user_id, lesson_id)
        rows = [
            dict(
                id=f"progress:{user_id}:{x.grade}",
                grade=x.grade,
                average_score=x.average_score,
                lesson_ids=[l.id for l in self.content.lessons(x.grade)],
            )
            for x in self.levels(user_id)
        ]
        self.repository.mark_lesson(user_id, lesson_id, True, rows)
        # Repository tính completion mới và ghi projection cùng transaction với COMPLETED.

    def refresh(self, user_id):
        self.identity.require_user(user_id)
        rows = [
            dict(
                id=f"progress:{user_id}:{x.grade}",
                grade=x.grade,
                completion=x.completion,
                average_score=x.average_score,
            )
            for x in self.levels(user_id)
        ]
        self.repository.projections(user_id, rows)

    def resume_lesson(self, user_id):
        self._user(user_id)
        id = self.repository.resume_id(user_id)
        if not id:
            return None
        for grade in (6, 7, 8, 9):
            if self.access(user_id, grade):
                lesson = next(
                    (l for l in self.content.lessons(grade) if l.id == id), None
                )
                if lesson:
                    return lesson
        return None

    def breakdown(self, user_id, grade):
        completed, _ = self.repository.snapshot(user_id)
        groups = {}
        for row in self.catalog_for(user_id, grade):
            for kind, key, name in [
                ("chapter", row.chapter_id, row.chapter_title),
                ("topic", row.lesson.topic_id, row.topic_title),
            ]:
                group = groups.setdefault(
                    (kind, key),
                    dict(kind=kind, id=key, title=name, total=0, completed=0),
                )
                group["total"] += 1
                group["completed"] += row.lesson.id in completed
        return [
            dict(x, completion=100 * x["completed"] / x["total"])
            for x in groups.values()
        ]

    def topic_statistics(self, user_id):
        self._user(user_id)
        groups = {}
        for a in self.assessment.attempts(user_id):
            if a.status == "completed" and 0 <= a.score <= 10:
                groups.setdefault(a.topic_id, []).append(a.score)
        return [
            dict(topic_id=k, attempts=len(v), average=mean(v), review=mean(v) < 5)
            for k, v in groups.items()
        ]

    def review_lessons(self, user_id):
        self._user(user_id)
        weak = {x["topic_id"] for x in self.topic_statistics(user_id) if x["review"]}
        completed, _ = self.repository.snapshot(user_id)
        result = {}
        for grade in (6, 7, 8, 9):
            for lesson in self.content.lessons(grade):
                if lesson.topic_id in weak:
                    for p in self.content.prerequisites(lesson.id):
                        if p.id not in completed and p.grade <= lesson.grade:
                            result[p.id] = p
        return sorted(result.values(), key=lambda x: (x.grade, x.id))
