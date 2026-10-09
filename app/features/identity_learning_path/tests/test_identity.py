from app.features.identity_learning_path.repositories.identity import IdentityRepository
from app.features.identity_learning_path.services.identity import IdentityService


class FakeDB:
    def __init__(self, rows):
        self.rows = rows

    def read(self, query, **params):
        self.params = params
        return self.rows


def test_missing_demo_user_is_none():
    assert (
        IdentityService(IdentityRepository(FakeDB([])), demo=True).current_user()
        is None
    )


def test_identity_uses_parameter_and_marks_demo():
    db = FakeDB([dict(id="user:demo-student", name="Demo", grade=8, role="student")])
    user = IdentityService(IdentityRepository(db), demo=True).current_user()
    assert user.demo is True
    assert user.grade == 8
    assert db.params == {"id": "user:demo-student"}
