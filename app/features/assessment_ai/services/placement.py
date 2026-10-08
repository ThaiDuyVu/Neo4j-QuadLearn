"""Placement question and scoring contract; grade recommendation belongs to Vũ."""

from collections import defaultdict
from random import SystemRandom

from ..models.placement import PlacementForm, PlacementGradeScore, PlacementResult
from ..models.quiz import AnswerResult, TestOption, TestQuestion
from .quiz import grade_answer
from .scoring import score


class PlacementService:
    def __init__(self, repository):
        self.repository = repository

    def form(self, grades: tuple[int, ...] = (6, 7, 8, 9),
             per_grade: int = 3) -> PlacementForm:
        if (not grades or len(set(grades)) != len(grades)
                or any(grade not in (6, 7, 8, 9) for grade in grades)
                or not 1 <= per_grade <= 10):
            raise ValueError("Cấu hình bài xếp loại không hợp lệ")
        grouped = defaultdict(list)
        for question in self.repository.placement_questions(grades):
            grouped[question.grade].append(question)
        missing = [grade for grade in grades if not grouped[grade]]
        if missing:
            raise ValueError("Chưa đủ câu hỏi đã xuất bản cho lớp: "
                             + ", ".join(map(str, missing)))
        rng = SystemRandom()
        selected = []
        for grade in grades:
            choices = grouped[grade]
            rng.shuffle(choices)
            selected.extend(choices[:per_grade])
        rng.shuffle(selected)
        return PlacementForm(tuple(
            TestQuestion(question.id, question.kind, question.text, question.image_url,
                         tuple(TestOption(option.id, option.text)
                               for option in question.options))
            for question in selected
        ))

    def grade(self, question_ids: tuple[str, ...],
              selections: dict[str, tuple[str, ...]]) -> PlacementResult:
        if (not question_ids or len(set(question_ids)) != len(question_ids)
                or set(selections) != set(question_ids)):
            raise ValueError("Bài xếp loại thiếu hoặc thừa câu trả lời")
        questions = self.repository.placement_questions_by_ids(question_ids)
        by_id = {question.id: question for question in questions}
        if set(by_id) != set(question_ids) or len(by_id) != len(questions):
            raise ValueError("Câu hỏi xếp loại không tồn tại hoặc chưa xuất bản")
        answers_by_grade: dict[int, list[AnswerResult]] = defaultdict(list)
        for question_id in question_ids:
            question = by_id[question_id]
            answers_by_grade[question.grade].append(
                grade_answer(question, selections[question_id]))
        scores = tuple(
            PlacementGradeScore(
                grade, sum(answer.correct for answer in answers), len(answers),
                score(sum(answer.correct for answer in answers), len(answers)))
            for grade, answers in sorted(answers_by_grade.items())
        )
        return PlacementResult(scores)
