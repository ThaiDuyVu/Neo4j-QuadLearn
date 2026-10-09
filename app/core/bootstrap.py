"""Composition root: chỉ vùng shared/core được nối các implementation của domain."""

from app.core.context import AppContext
from app.features.identity_learning_path.repositories.identity import IdentityRepository
from app.features.identity_learning_path.services.identity import IdentityService
from app.features.learning_geometry.repositories.content import ContentRepository
from app.features.learning_geometry.services.content import ContentService
from app.features.assessment_ai.repositories.assessment import AssessmentRepository
from app.features.assessment_ai.services.assessment import AssessmentService

from app.core.catalog import GraphLearningCatalog
from app.features.identity_learning_path.services.auth import AuthService
from app.features.identity_learning_path.services.learning_path import (
    LearningPathService,
)
from app.features.identity_learning_path.repositories.progress import ProgressRepository
from app.features.identity_learning_path.models.policy import IdentityPolicy


def build_context(database, session_state=None, demo=False):
    repository = IdentityRepository(database)
    policy = IdentityPolicy.load()
    identity = IdentityService(repository, session_state, policy, demo=demo)
    content = ContentService(ContentRepository(database))
    assessment = AssessmentService(AssessmentRepository(database), identity=identity)
    progress = LearningPathService(
        ProgressRepository(database),
        identity,
        content,
        assessment,
        GraphLearningCatalog(database),
        policy,
    )
    return AppContext(
        identity, content, assessment, AuthService(repository, policy), progress
    )
