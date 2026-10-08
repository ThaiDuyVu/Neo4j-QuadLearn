from dataclasses import dataclass
from app.shared.contracts.ports import IdentityReader, ContentReader, AssessmentReader

@dataclass(frozen=True)
class AppContext:
    identity: IdentityReader
    content: ContentReader
    assessment: AssessmentReader
