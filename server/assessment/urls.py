from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assessment.views import * 
router = DefaultRouter()

router.register(r'assessments', AssessmentViewSet, basename='assessments')
router.register(r'assessment-questions', AssessmentQuestionViewSet, basename='assessment-questions')
router.register(r'assessment-choices', AssessmentChoiceViewSet, basename='assessment-choices')
router.register(r'assessment-attempts', AssessmentAttemptViewSet, basename='assessment-attempts')
router.register(r'assessment-answers', AssessmentAnswerViewSet, basename='assessment-answers')
router.register(r'assessment-results', AssessmentResultViewSet, basename='assessment-results')
router.register(r'assessment-types', AssessmentTypeViewSet, basename='assessment-types')
router.register(r'submission-types', SubmissionTypeViewSet, basename='submission-types')

urlpatterns = [
    path('api/', include(router.urls)),
]