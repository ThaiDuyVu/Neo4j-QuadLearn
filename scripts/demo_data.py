"""Local demo fixtures: python -m scripts.demo_data [--reset-demo-users --yes].

Composition script nối các domain qua bootstrap; không thay đổi quyền ghi runtime.
Mật khẩu mặc định là credential công khai chỉ cho tài khoản dữ liệu thử nghiệm.
"""
import argparse
import json
import os
from pathlib import Path

from app.core.bootstrap import build_context
from app.core.config import ROOT, Settings
from app.core.database import Database
from app.features.identity_learning_path.services.security import validate_password
from app.shared.utils.cypher import statements

PACK = 'quadlearn-demo-v1'
DEFAULT_PASSWORD = 'Demo123456789'
ACCOUNTS = [
    ('start', 'Người học bắt đầu', 8, [], None),
    ('path', 'Người học đang học', 8, ['parallelogram', 'rectangle'], True),
    ('ready', 'Người học sẵn sàng chuyển cấp', 8, ['parallelogram', 'rectangle', 'rhombus'], True),
    ('review', 'Người học cần ôn tập', 8, [], False),
    ('junior', 'Người học lớp 6', 6, ['rectangle'], True),
    ('senior', 'Người học lớp 9', 9, ['cyclic'], True),
    ('manager', 'Quản trị demo', 8, [], None),
]


def load_content(path: Path = ROOT / 'database/demo/content.json'):
    data = json.loads(path.read_text(encoding='utf-8'))
    lessons = {x['id']: x for x in data['lessons']}
    if len(lessons) != len(data['lessons']):
        raise ValueError('Trùng lesson ID')
    topics = {x['topic_id']: x['grade'] for x in lessons.values()}
    ids = set(lessons)
    for lesson in lessons.values():
        if lesson['grade'] not in (6, 7, 8, 9) or not lesson['content_vi'].strip():
            raise ValueError('Bài học thiếu nội dung hoặc sai lớp')
        if any(p not in lessons or lessons[p]['grade'] > lesson['grade']
               for p in lesson['prerequisites']):
            raise ValueError('Tiên quyết không tồn tại hoặc vượt lớp')
    def visit(lid, stack):
        if lid in stack:
            raise ValueError('Chu trình tiên quyết')
        for prerequisite in lessons[lid]['prerequisites']:
            visit(prerequisite, stack | {lid})
    for lid in lessons:
        visit(lid, set())
    for label in ('questions', 'essays'):
        for item in data[label]:
            if item['id'] in ids or topics.get(item['topic_id']) != item['grade']:
                raise ValueError('Trùng ID hoặc chủ đề sai lớp')
            ids.add(item['id'])
            if label == 'questions':
                if len(item['options']) < 2 or sum(o['correct'] for o in item['options']) != 1:
                    raise ValueError('Câu single phải có đúng một đáp án đúng')
                for option in item['options']:
                    if option['id'] in ids:
                        raise ValueError('Trùng option ID')
                    ids.add(option['id'])
            elif not item['hints'] or not item['solution_vi']:
                raise ValueError('Tự luận thiếu gợi ý/lời giải')
    return data


def import_content(db, data):
    # Chỉ chuẩn hóa bộ seed demo có ID đã biết; không ghi đè nội dung thực của người dùng.
    def work(tx):
        for item in data['lessons']:
            for label, key in [('Lesson', 'id'), ('Topic', 'topic_id')]:
                row = tx.run(f'MATCH (n:{label} {{id:$id}}) RETURN n.demo AS demo',
                             id=item[key]).single()
                if row and row['demo'] is not True:
                    raise ValueError(f'ID đã thuộc nội dung khác: {item[key]}')
            tx.run('''
                MATCH (level:Level {grade:$grade})
                MERGE (chapter:Chapter {id:$chapter})
                ON CREATE SET chapter.name_vi=$chapter_title,chapter.grade=$grade,
                              chapter.order=1,chapter.demo=true,chapter.status='published'
                MERGE (level)-[:HAS_CHAPTER]->(chapter)
                MERGE (topic:Topic {id:$topic_id})
                SET topic.name_vi=$title_vi,topic.grade=$grade,topic.status='published',
                    topic.order=$order,topic.cognitive_level='understand',topic.demo=true
                MERGE (chapter)-[:HAS_TOPIC]->(topic)
                MERGE (lesson:Lesson {id:$id})
                SET lesson.title_vi=$title_vi,lesson.title_en=$title_en,
                    lesson.content_vi=$content_vi,lesson.content_en=$content_en,
                    lesson.grade=$grade,lesson.order=$order,lesson.status='published',
                    lesson.demo=true,lesson.demo_pack=$pack
                MERGE (topic)-[:HAS_LESSON]->(lesson)
            ''', **{k:v for k,v in item.items() if k not in ('prerequisites','shape_id')},
                chapter=f"chapter:{item['grade']}:demo",
                chapter_title=f"Nội dung minh họa lớp {item['grade']}", pack=PACK).consume()
            if item['shape_id']:
                tx.run('''MATCH (l:Lesson {id:$id}), (q:Quadrilateral {id:$shape})
                          MERGE (l)-[:ABOUT]->(q)''', id=item['id'],shape=item['shape_id']).consume()
        for item in data['lessons']:
            for prerequisite in item['prerequisites']:
                tx.run('''MATCH (l:Lesson {id:$id}),(p:Lesson {id:$pre})
                          MERGE (l)-[:REQUIRES]->(p)''',id=item['id'],pre=prerequisite).consume()
        for item in data['questions']:
            ensure_demo(tx, 'Question', item['id'])
            tx.run('''MATCH (t:Topic {id:$topic_id}) MERGE (q:Question {id:$id})
                      SET q.grade=$grade,q.type=$type,q.difficulty=$difficulty,
                          q.text_vi=$text_vi,q.explanation_vi=$explanation_vi,
                          q.status='published',q.demo=true,q.demo_pack=$pack
                      MERGE (t)-[:HAS_QUESTION]->(q)''',
                   **{k:v for k,v in item.items() if k!='options'},pack=PACK).consume()
            for option in item['options']:
                ensure_demo(tx,'Option',option['id'])
                tx.run('''MATCH (q:Question {id:$question}) MERGE (o:Option {id:$id})
                          SET o.text_vi=$text_vi,o.correct=$correct,o.demo=true,o.demo_pack=$pack
                          MERGE (q)-[:HAS_OPTION]->(o)''',
                       **option,question=item['id'],pack=PACK).consume()
        for item in data['essays']:
            ensure_demo(tx,'EssayProblem',item['id'])
            tx.run('''MATCH (t:Topic {id:$topic_id}) MERGE (e:EssayProblem {id:$id})
                      SET e.grade=$grade,e.kind=$kind,e.prompt_vi=$prompt_vi,
                          e.assumptions_vi=$assumptions_vi,e.conclusion_vi=$conclusion_vi,
                          e.solution_vi=$solution_vi,e.demo=true,e.status='published',e.demo_pack=$pack
                      MERGE (t)-[:HAS_ESSAY]->(e)''',
                   **{k:v for k,v in item.items() if k!='hints'},pack=PACK).consume()
            for order,hint in enumerate(item['hints'],1):
                hid=('hint:rectangle:1' if item['id']=='essay:8:rectangle:1' and order==1
                     else f"hint:demo:{item['id']}:{order}")
                ensure_demo(tx,'EssayHint',hid)
                tx.run('''MATCH (e:EssayProblem {id:$essay}) MERGE (h:EssayHint {id:$id})
                          SET h.order=$order,h.text_vi=$text,h.demo=true,h.demo_pack=$pack
                          MERGE (e)-[:HAS_HINT]->(h)''',
                       essay=item['id'],id=hid,order=order,text=hint,pack=PACK).consume()
    db.transaction(work)


def ensure_demo(tx, label, identifier):
    row=tx.run(f'MATCH (n:{label} {{id:$id}}) RETURN n.demo AS demo',id=identifier).single()
    if row and row['demo'] is not True:
        raise ValueError(f'ID đã thuộc dữ liệu khác: {identifier}')


def reset_accounts(db):
    # Chỉ fixture User được script đánh dấu; KHÔNG duyệt qua Lesson/Topic dùng chung.
    db.write('''MATCH (u:User {fixture_pack:$pack})
                OPTIONAL MATCH (u)-[:HAS_AUTH_SESSION|HAS_AUTH_TOKEN|HAS_PROGRESS|ATTEMPTED|HAS_CHAT|REVIEWED_ESSAY]->(owned)
                OPTIONAL MATCH (owned)-[:HAS_ANSWER|HAS_MESSAGE]->(child)
                WITH collect(DISTINCT u)+collect(DISTINCT owned)+collect(DISTINCT child) AS nodes
                UNWIND nodes AS n DETACH DELETE n''',pack=PACK)
    db.write('''MATCH (q:AIQuotaDay) WHERE q.user_id IN $ids DETACH DELETE q''',
             ids=[f'user:fixture:{key}' for key,*_ in ACCOUNTS])


def ensure_accounts(db,password):
    for key,name,grade,completed,correct in ACCOUNTS:
        uid=f'user:fixture:{key}'; email=f'demo.{key}@quadlearn.local'
        existing=db.read('MATCH (u:User) WHERE u.id=$id OR u.email=$email RETURN u.id AS id,u.fixture_pack AS pack,u.fixture_initialized AS initialized',id=uid,email=email)
        if existing:
            if len(existing)!=1 or existing[0]['id']!=uid or existing[0]['pack']!=PACK:
                raise ValueError(f'Không ghi đè tài khoản ngoài bộ demo: {email}')
            if existing[0]['initialized']:
                print(f'Giữ trạng thái: {email}')
                continue
        ctx=build_context(db,session_state={})
        if not existing:
            # Tài khoản thử nghiệm 18 tuổi: không giả lập xác nhận của người giám hộ thật.
            created,delivery=ctx.auth.register(name,email,password,grade,18)
            ctx.auth.activate(delivery['verify'],'verify')
            db.write('MATCH (u:User {id:$created}) SET u.id=$id,u.fixture_pack=$pack,u.role=$role',
                     created=created,id=uid,pack=PACK,role='admin' if key=='manager' else 'student')
            # register đã tạo projection theo ID ban đầu: cập nhật cùng định danh fixture.
            db.write('''MATCH (u:User {id:$id})-[:HAS_PROGRESS]->(p:Progress)-[:FOR_LEVEL]->(l:Level)
                        SET p.user_id=$id,p.id='progress:'+$id+':'+toString(l.grade)''',id=uid)
        token=ctx.auth.login(email,password)
        ctx.identity.login(token)
        try:
            for lesson in completed:
                ctx.progress.complete_lesson(uid,f'lesson:{grade}:{lesson}')
            if key=='path':
                ctx.progress.start_lesson(uid,'lesson:8:rhombus')
            # Rerun sau lỗi không tạo thêm bài làm fixture nếu đã có bài hoàn tất.
            if correct is not None and not ctx.assessment.attempts(uid):
                topic=f'topic:{grade}:'+{6:'rectangle',8:'rectangle',9:'cyclic'}[grade]
                questions=ctx.assessment.questions(grade,topic)
                selections={q.id:tuple(o.id for o in q.options if o.correct==correct)[:1]
                            for q in questions}
                ctx.assessment.submit(uid,topic,selections)
            ctx.progress.refresh(uid)
            db.write('MATCH (u:User {id:$id}) SET u.fixture_initialized=true',id=uid)
            print(f'Đã tạo: {email} · lớp {grade}')
        finally:
            ctx.identity.logout()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reset-demo-users',action='store_true',help='Xóa và tạo lại CHỈ tài khoản fixture và lịch sử của chúng')
    parser.add_argument('--yes',action='store_true',help='Xác nhận reset tài khoản fixture')
    args=parser.parse_args()
    settings=Settings.load()
    if settings.app_env!='development':
        parser.error('Chỉ chạy khi APP_ENV=development')
    if args.reset_demo_users and not args.yes:
        parser.error('Reset cần --reset-demo-users --yes; lịch sử fixture sẽ bị xóa')
    password=os.getenv('QUADLEARN_DEMO_PASSWORD',DEFAULT_PASSWORD)
    validate_password(password)
    data=load_content()
    db=Database(settings)
    try:
        db.verify()
        db.apply(statements(ROOT/'database/constraints.cypher'))
        grades = {row['grade'] for row in db.read('MATCH (l:Level) RETURN l.grade AS grade')}
        if not {6, 7, 8, 9} <= grades:
            parser.error('Chạy python -m scripts.db init trước để tạo graph nền')
        import_content(db,data)
        if args.reset_demo_users:
            reset_accounts(db)
        ensure_accounts(db,password)
        print(f"Nội dung: {len(data['lessons'])} bài, {len(data['questions'])} câu hỏi, {len(data['essays'])} tự luận.")
        print('Mật khẩu fixture: mặc định công khai trong docs/DEMO_DATA.md; nếu override, dùng biến QUADLEARN_DEMO_PASSWORD.')
    finally:
        db.close()

if __name__=='__main__':
    main()
