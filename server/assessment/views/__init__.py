from .assessment_answer_views import AssessmentAnswerViewSet
from .assessment_attempt_views import AssessmentAttemptViewSet
from .assessment_choice_views import AssessmentChoiceViewSet
from .assessment_question_views import AssessmentQuestionViewSet
from .assessment_result_views import AssessmentResultViewSet
from .assessment_views import AssessmentViewSet
from .assessment_type_views import QuestionTypeViewSet
from .submission_views import SubmissionTypeViewSet

__all__ = [
            "AssessmentAnswerViewSet",
            "AssessmentAttemptViewSet",
            "AssessmentChoiceViewSet",
            "AssessmentQuestionViewSet",
            "AssessmentResultViewSet",
            "AssessmentViewSet",
            "QuestionTypeViewSet",
            "SubmissionTypeViewSet"
        ]
