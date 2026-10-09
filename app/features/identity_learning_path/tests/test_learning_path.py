import pytest
from app.shared.models.dto import CurrentUser, AttemptSummary
from app.features.identity_learning_path.services.learning_path import (
    LearningPathService,
)
from app.features.identity_learning_path.models.errors import IdentityError
from app.features.identity_learning_path.models.policy import IdentityPolicy
from .fakes import Content, Assessment, MemoryProgressRepository


class Identity:
    def __init__(self):
        self.user = CurrentUser("user:test", "Student", 6, "student", False)
        self.repository = self

    def current_user(self):
        return self.user

    def profile(self, uid):
        return dict(starting_grade=6)

    def require_user(self, uid=None):
        if self.user.demo or uid and uid != self.user.id:
            raise IdentityError("Unauthorized")
        return self.user


@pytest.fixture
def env():
    repo = MemoryProgressRepository()
    identity = Identity()
    content = Content()
    assessment = Assessment()
    service = LearningPathService(repo, identity, content, assessment, content)
    return repo, identity, content, assessment, service


def test_completion_published_denominator_and_empty_grade(env):
    repo, identity, content, assessment, service = env
    repo.completed = {"lesson:6:a", "lesson:draft:removed"}
    levels = service.levels("user:test")
    assert levels[0].total == 2 and levels[0].completion == 50
    assert levels[2].completion == 0 and levels[2].average_score is None


@pytest.mark.parametrize(
    "completion,score,allowed",
    [(1, 6, False), (2, 5.99, False), (2, 6, True), (2, None, False)],
)
def test_unlock_requires_completion_score_and_previous_level(
    env, completion, score, allowed
):
    repo, identity, content, assessment, service = env
    repo.completed = {l.id for l in content.lessons(6)[:completion]}
    assessment.items = (
        [] if score is None else [AttemptSummary("a", "topic:6:a", score, "completed")]
    )
    assert service.access("user:test", 7) == allowed
    assert not service.access("user:test", 8)


def test_threshold_exact_boundary_configurable(env):
    repo, identity, content, assessment, service = env
    repo.completed = {"lesson:6:a"}
    assessment.items = [AttemptSummary("a", "topic:6:a", 6, "completed")]
    service.policy = IdentityPolicy(completion_threshold=50)
    assert service.access("user:test", 7)


def test_average_all_or_latest_excludes_draft_unknown_topic(env):
    repo, identity, content, assessment, service = env
    assessment.items = [
        AttemptSummary("new", "topic:6:a", 8, "completed"),
        AttemptSummary("old", "topic:6:a", 2, "completed"),
        AttemptSummary("draft", "topic:6:b", 0, "draft"),
        AttemptSummary("unknown", "other", 10, "completed"),
    ]
    assert service.levels("user:test")[0].average_score == 5
    service.policy = IdentityPolicy(average_policy="latest")
    assert service.levels("user:test")[0].average_score == 8


def test_skip_requires_explicit_confirmation_and_lower_levels_free(env):
    repo, identity, content, assessment, service = env
    with pytest.raises(IdentityError):
        service.change_level(9)
    service.change_level(9, True)
    assert repo.changed[2] == "confirmed_skip"
    identity.user = CurrentUser("user:test", "Student", 9, "student", False)
    assert all(service.access("user:test", grade) for grade in (6, 7, 8, 9))


def test_skip_disabled_and_invalid_grade(env):
    service = env[4]
    service.policy = IdentityPolicy(allow_skip=False)
    with pytest.raises(IdentityError):
        service.change_level(9, True)
    with pytest.raises(IdentityError):
        service.access("user:test", 5)


def test_complete_is_idempotent_and_refreshes_projection(env):
    repo, identity, content, assessment, service = env
    service.complete_lesson("user:test", "lesson:6:a")
    service.complete_lesson("user:test", "lesson:6:a")
    assert repo.completed == {"lesson:6:a"}
    assert repo.rows[0]["completion"] == 50
    assert all(row["id"].startswith("progress:user:test:") for row in repo.rows)


def test_cannot_write_other_user_or_locked_or_nonexistent_lesson(env):
    service = env[4]
    for uid, lid in [
        ("user:other", "lesson:6:a"),
        ("user:test", "lesson:7:a"),
        ("user:test", "lesson:missing"),
    ]:
        with pytest.raises(IdentityError):
            service.complete_lesson(uid, lid)
    assert env[0].writes == 0


def test_demo_is_readonly(env):
    repo, identity, content, assessment, service = env
    identity.user = CurrentUser("user:test", "Demo", 6, "student", True)
    assert service.levels("user:test")
    with pytest.raises(IdentityError):
        service.complete_lesson("user:test", "lesson:6:a")


def test_resume_and_chapter_topic_breakdown(env):
    repo, identity, content, assessment, service = env
    service.start_lesson("user:test", "lesson:6:b")
    assert service.resume_lesson("user:test").id == "lesson:6:b"
    repo.completed = {"lesson:6:a"}
    chapter = next(
        x for x in service.breakdown("user:test", 6) if x["kind"] == "chapter"
    )
    assert chapter["completion"] == 50


def test_review_multihop_unfinished_prerequisites(env):
    repo, identity, content, assessment, service = env
    assessment.items = [AttemptSummary("a", "topic:7:a", 4, "completed")]
    repo.completed = {"lesson:6:a"}
    assert [l.id for l in service.review_lessons("user:test")] == ["lesson:6:b"]


def test_policy_validation():
    for kwargs in [
        dict(session_days=0),
        dict(completion_threshold=101),
        dict(score_threshold=11),
        dict(average_policy="best"),
    ]:
        with pytest.raises(ValueError):
            IdentityPolicy(**kwargs)


def test_seventy_percent_six_points_exact_srs_boundary(env):
    from app.shared.models.dto import LessonSummary

    repo, identity, content, assessment, service = env
    content.items[6] = [
        LessonSummary(f"lesson:6:{i}", str(i), 6, "topic:6:a") for i in range(10)
    ]
    repo.completed = {l.id for l in content.items[6][:7]}
    assessment.items = [AttemptSummary("a", "topic:6:a", 6, "completed")]
    assert service.levels("user:test")[0].completion == 70
    assert service.access("user:test", 7)
    repo.completed.remove("lesson:6:6")
    assert not service.access("user:test", 7)


def test_previously_opened_higher_level_keeps_lower_levels_available(env):
    repo, identity, content, assessment, service = env
    repo.opened["user:test"] = {9}
    assert all(service.access("user:test", grade) for grade in [6, 7, 8, 9])
