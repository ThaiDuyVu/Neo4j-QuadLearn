"""Composition root: chỉ vùng shared/core được nối các implementation của domain."""
from app.core.context import AppContext
from app.features.identity_learning_path.repositories.identity import IdentityRepository
from app.features.identity_learning_path.services.identity import IdentityService
from app.features.learning_geometry.repositories.content import ContentRepository
from app.features.learning_geometry.services.content import ContentService
from app.features.assessment_ai.repositories.assessment import AssessmentRepository
from app.features.assessment_ai.services.assessment import AssessmentService

def build_context(database):
    return AppContext(IdentityService(IdentityRepository(database)),
                      ContentService(ContentRepository(database)),
                      AssessmentService(AssessmentRepository(database)))
