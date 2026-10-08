from dataclasses import dataclass
from app.shared.contracts.ports import (
    IdentityReader,
    ContentReader,
    AssessmentReader,
    Authentication,
    LearningPath,
)


@dataclass(frozen=True)
class AppContext:
    identity: IdentityReader
    content: ContentReader
    assessment: AssessmentReader

    auth: Authentication | None = None
    progress: LearningPath | None = None
