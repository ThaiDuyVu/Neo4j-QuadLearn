from app.core.context import AppContext
from app.shared.models.dto import CurrentUser, LessonSummary, AttemptSummary

class FakeIdentity:
    def current_user(self): return CurrentUser("user:test", "Demo", 8, "student")
class FakeContent:
    def lessons(self, grade): return [LessonSummary("lesson:test", "Rectangle", grade, "topic:test", "Demo content")]
    def prerequisites(self, lesson_id): return [LessonSummary("lesson:base", "Parallel", 7, "topic:base")]
    def ai_context(self, lesson_id): return self.lessons(8)
class FakeAssessment:
    def attempts(self, user_id): return [AttemptSummary("attempt:test", "topic:test", 10, "completed")]
def context(): return AppContext(FakeIdentity(), FakeContent(), FakeAssessment())
