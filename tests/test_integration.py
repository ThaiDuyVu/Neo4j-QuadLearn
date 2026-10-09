import os
from pathlib import Path
import pytest
from app.core.config import Settings
from app.core.database import Database
from app.core.bootstrap import build_context
from app.shared.utils.cypher import statements

pytestmark = [pytest.mark.integration, pytest.mark.skipif(os.getenv("QUADLEARN_INTEGRATION") != "1", reason="Requires explicit local demo DB opt-in")]

@pytest.fixture
def db():
    database = Database(Settings.load())
    database.verify()
    yield database
    database.close()

def counts(db):
    return (db.read("MATCH (n) RETURN count(n) AS n")[0]["n"],
            db.read("MATCH ()-[r]->() RETURN count(r) AS n")[0]["n"])

def test_seed_idempotent_nodes_and_relationships(db):
    before = counts(db)
    db.apply(statements(Path("database/seed.cypher")))
    assert counts(db) == before

def test_domain_contracts_and_multihop(db):
    ctx = build_context(db, demo=True)
    user = ctx.identity.current_user()
    assert user.grade == 8
    assert {"lesson:8:parallelogram", "lesson:8:rectangle"} <= {
        lesson.id for lesson in ctx.content.lessons(8)
    }
    prereqs = ctx.content.prerequisites("lesson:9:cyclic")
    assert {item.grade for item in prereqs} == {6,7,8}
    assert ctx.assessment.attempts(user.id)[0].score == 10
    assert len(ctx.content.ai_context("lesson:8:rectangle")) >= 3
    shape = db.read("MATCH (:Quadrilateral {id:'shape:square'})-[:IS_A*1..5]->(q) RETURN DISTINCT q.id AS id")
    assert {"shape:rhombus", "shape:rectangle", "shape:parallelogram"} <= {r['id'] for r in shape}

def test_example_queries_execute(db):
    for query in statements(Path("database/examples.cypher")):
        db.read(query)

def test_option_answer_ownership_consistent(db):
    invalid = db.read("MATCH (a:AttemptAnswer)-[:ANSWERS]->(q:Question), (a)-[:SELECTED]->(o:Option) WHERE NOT EXISTS { MATCH (q)-[:HAS_OPTION]->(o) } RETURN a.id AS id")
    assert invalid == []
