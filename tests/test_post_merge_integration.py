"""Luồng thật xuyên ba domain, dữ liệu user riêng và cleanup theo owner fixture."""
import os
from uuid import uuid4
import pytest
from app.core.bootstrap import build_context
from app.core.config import Settings
from app.core.database import Database

pytestmark = [pytest.mark.integration,pytest.mark.skipif(os.getenv('QUADLEARN_INTEGRATION')!='1',reason='Local Neo4j opt-in')]


def test_authenticated_learning_quiz_progress_chat_and_revocation():
    db = Database(Settings.load())
    uid = None
    try:
        db.verify()
        ctx = build_context(db,session_state={})
        email = f'audit-{uuid4()}@example.invalid'
        uid,tokens = ctx.auth.register('Audit student',email,'TestPass123',8,18)
        ctx.auth.activate(tokens['verify'],'verify')
        ctx.identity.login(ctx.auth.login(email,'TestPass123'))
        assert ctx.identity.current_user().id == uid
        source = ctx.content.get_lesson('lesson:8:rectangle')
        assert source and source.topic_id == 'topic:8:rectangle'
        question = next(q for q in ctx.assessment.questions(8,source.topic_id) if q.id=='question:8:rectangle:1')
        correct = next(o.id for o in question.options if o.correct)
        result = ctx.assessment.submit(uid,source.topic_id,{question.id:(correct,)})
        assert result.score == 10
        assert ctx.assessment.attempt_detail(uid,result.id)[0]['selected_ids'] == [correct]
        ctx.progress.start_lesson(uid,source.id)
        assert ctx.progress.resume_lesson(uid).id == source.id
        ctx.progress.complete_lesson(uid,source.id)
        # Hoàn thành catalog hiện tại; không giả định seed chỉ có hai bài.
        for lesson in ctx.content.lessons(8):
            ctx.progress.complete_lesson(uid,lesson.id)
        level8 = ctx.progress.levels(uid)[2]
        assert level8.completion == 100 and level8.average_score == 10
        assert ctx.progress.access(uid,9)
        ctx.progress.refresh(uid)
        projection = db.read('MATCH (:User {id:$id})-[:HAS_PROGRESS]->(p)-[:FOR_LEVEL]->(:Level {grade:8}) RETURN p.completion AS completion,p.average_score AS score',id=uid)[0]
        assert projection == {'completion':100.0,'score':10.0}
        from app.features.assessment_ai.models.ai import AIRequest
        context = tuple(ctx.content.ai_context(source.id))
        reply = ctx.assessment.ask_ai(uid,AIRequest('Giải thích hình chữ nhật',8,'vi',context,source.id))
        assert reply.source_ids and ctx.assessment.chat_messages(uid,reply.session_id)
        ctx.assessment.chat_feedback(uid,ctx.assessment.chat_messages(uid,reply.session_id)[-1]['id'],'helpful')
        with pytest.raises(ValueError): ctx.assessment.attempts('user:demo-student')
        with pytest.raises(ValueError): ctx.assessment.preview_assessment(source.topic_id)
        # Mô phỏng trạng thái bị admin khóa tại nguồn identity; phiên phải bị từ chối.
        db.write('MATCH (u:User {id:$id}) SET u.status="blocked",u.auth_version=coalesce(u.auth_version,0)+1',id=uid)
        with pytest.raises(ValueError): ctx.assessment.submit(uid,source.topic_id,{question.id:(correct,)})
        assert db.read('MATCH (:User {id:$id})-[:ATTEMPTED]->(a) RETURN count(a) AS n',id=uid)[0]['n'] == 1
    finally:
        if uid:
            db.write('MATCH (:User {id:$id})-[:ATTEMPTED]->(:Attempt)-[:HAS_ANSWER]->(x:AttemptAnswer) DETACH DELETE x',id=uid)
            db.write('MATCH (:User {id:$id})-[:HAS_CHAT]->(:ChatSession)-[:HAS_MESSAGE]->(m:ChatMessage) DETACH DELETE m',id=uid)
            db.write('MATCH (:User {id:$id})-[:ATTEMPTED|HAS_CHAT|HAS_AUTH_TOKEN|HAS_AUTH_SESSION|HAS_PROGRESS]->(n) DETACH DELETE n',id=uid)
            db.write('MATCH (q:AIQuotaDay {user_id:$id}) DETACH DELETE q',id=uid)
            db.write('MATCH (u:User {id:$id}) DETACH DELETE u',id=uid)
        db.close()


def test_composed_demo_cannot_persist_assessment_or_read_other_identity():
    db = Database(Settings.load())
    try:
        ctx = build_context(db,demo=True)
        uid = ctx.identity.current_user().id
        with pytest.raises(ValueError): ctx.assessment.submit(uid,'topic:8:rectangle',{})
        with pytest.raises(ValueError): ctx.assessment.ask_ai(uid,None)
        with pytest.raises(ValueError): ctx.assessment.attempts('user:someone-else')
    finally:
        db.close()


def test_draft_parent_is_not_content_context_or_progress_denominator():
    db = Database(Settings.load())
    prefix = f'audit:{uuid4()}'
    chapter,topic,lesson = (prefix+':chapter',prefix+':topic',prefix+':lesson')
    try:
        ctx = build_context(db,demo=True)
        before = ctx.content.lessons(8)
        db.write('''MATCH (v:Level {grade:8})
CREATE (v)-[:HAS_CHAPTER]->(c:Chapter {id:$chapter,status:'draft',grade:8})
CREATE (c)-[:HAS_TOPIC]->(t:Topic {id:$topic,status:'published',grade:8})
CREATE (t)-[:HAS_LESSON]->(l:Lesson {id:$lesson,status:'published',grade:8,title_vi:'Draft parent',content_vi:'Hidden'})
CREATE (l)-[:REQUIRES]->(:Lesson {id:$prereq,status:'published',grade:7,title_vi:'Unlinked'})''',
                 chapter=chapter,topic=topic,lesson=lesson,prereq=prefix+':pre')
        assert ctx.content.lessons(8) == before
        assert ctx.content.get_lesson(lesson) is None
        assert all(x.lesson.id != lesson for x in ctx.progress.catalog_for('user:demo-student',8))
        assert ctx.progress.levels('user:demo-student')[2].total == len(before)
    finally:
        db.write('MATCH (n) WHERE n.id IN $ids DETACH DELETE n',ids=[chapter,topic,lesson,prefix+':pre'])
        db.close()
