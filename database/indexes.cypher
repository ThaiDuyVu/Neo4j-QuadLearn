CREATE INDEX lesson_grade_status IF NOT EXISTS FOR (l:Lesson) ON (l.grade, l.status)
;
CREATE INDEX topic_code_grade IF NOT EXISTS FOR (t:Topic) ON (t.code, t.grade)
;
CREATE INDEX attempt_status IF NOT EXISTS FOR (a:Attempt) ON (a.status)
;
CREATE INDEX chat_message_time IF NOT EXISTS FOR (m:ChatMessage) ON (m.created_at)
;
