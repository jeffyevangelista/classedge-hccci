from rest_framework.viewsets import ModelViewSet
from assessment.models import AssessmentAnswer, Assessment, AssessmentAttempt, AssessmentQuestion, AssessmentChoice, AssessmentResult
from assessment.serializers import AssessmentAnswerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal
from django.db import transaction, models
from rest_framework import status
from common.pagination import CustomPagination
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class AssessmentAnswerViewSet(ModelViewSet):
    serializer_class = AssessmentAnswerSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    @action(detail=False, methods=['post'], url_path='submit')
    @transaction.atomic
    def submit_assessment(self, request):
        student_id = request.data.get('student_id')
        assessment_id = request.data.get('assessment_id')
        answers = request.data.get('answers', []) 

        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

        attempt_number = AssessmentAttempt.objects.filter(
            assessment=assessment, student=student_id
        ).count() + 1

        attempt = AssessmentAttempt.objects.create(
            assessment=assessment,
            student=student_id,
            attempt_number=attempt_number,
            is_late=False,
            score=Decimal('0.00'),
            penalty_applied=Decimal('0.00'),
            final_score=Decimal('0.00')
        )

        total_score = Decimal('0.00')
        for ans in answers:
            try:
                question = AssessmentQuestion.objects.get(id=ans['question_id'])
            except AssessmentQuestion.DoesNotExist:
                continue

            choice = AssessmentChoice.objects.filter(id=ans.get('choice_id')).first()
            score_awarded = Decimal('0.00')
            grading_status = 'pending_review'

            # Auto-grade multiple choice questions
            if choice:
                if choice.is_correct:
                    score_awarded = question.points
                grading_status = 'auto_graded'

            AssessmentAnswer.objects.create(
                attempt=attempt,
                question=question,
                assessment_choice=choice,
                answer_text=ans.get('answer_text', ''),
                score_awarded=score_awarded,
                grading_status=grading_status
            )

            # Only add auto-graded scores to total
            if grading_status == 'auto_graded':
                total_score += score_awarded

        penalty = Decimal('0.00')
        if attempt.is_late:
            penalty = (assessment.late_penalty_percent / Decimal('100')) * total_score

        final_score = total_score - penalty
        attempt.score = total_score
        attempt.penalty_applied = penalty
        attempt.final_score = final_score
        attempt.save()

        update_assessment_result(assessment, student_id)

        return Response({
            "message": "Assessment submitted successfully",
            "attempt_id": attempt.id,
            "total_score": str(total_score),
            "final_score": str(final_score),
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='grade')
    @transaction.atomic
    def grade_answer(self, request, pk=None):
        """Grade a single answer (for essay/text questions)"""
        try:
            answer = AssessmentAnswer.objects.get(id=pk)
        except AssessmentAnswer.DoesNotExist:
            return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        score_awarded = request.data.get('score_awarded')
        feedback = request.data.get('feedback', '')
        
        if score_awarded is None:
            return Response({'error': 'score_awarded is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            score_awarded = Decimal(str(score_awarded))
        except (ValueError, TypeError):
            return Response({'error': 'Invalid score format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate score doesn't exceed question points
        if score_awarded > answer.question.points:
            return Response(
                {'error': f'Score cannot exceed {answer.question.points} points'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if score_awarded < 0:
            return Response({'error': 'Score cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update answer
        answer.score_awarded = score_awarded
        answer.feedback = feedback
        answer.grading_status = 'graded'
        answer.graded_by = request.user
        answer.graded_at = timezone.now()
        answer.save()
        
        # Recalculate attempt score
        recalculate_attempt_score(answer.attempt)
        
        # Update assessment result
        update_assessment_result(answer.attempt.assessment, answer.attempt.student)
        
        return Response({
            'message': 'Answer graded successfully',
            'answer_id': answer.id,
            'score_awarded': str(answer.score_awarded),
            'new_attempt_score': str(answer.attempt.final_score)
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='ungraded')
    def get_ungraded_answers(self, request):
        """Get all answers pending review for an assessment"""
        assessment_id = request.query_params.get('assessment_id')
        
        if not assessment_id:
            return Response({'error': 'assessment_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        answers = AssessmentAnswer.objects.filter(
            grading_status='pending_review',
            attempt__assessment_id=assessment_id
        ).select_related('attempt', 'question', 'attempt__student').order_by('created_at')
        
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='attempt-answers')
    def get_attempt_answers(self, request):
        """Get all answers for a specific attempt"""
        attempt_id = request.query_params.get('attempt_id')
        
        if not attempt_id:
            return Response({'error': 'attempt_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        answers = AssessmentAnswer.objects.filter(
            attempt_id=attempt_id
        ).select_related('question', 'assessment_choice').order_by('question__order_index')
        
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def recalculate_attempt_score(attempt):
    """Recalculate total score for an attempt after grading"""
    answers = AssessmentAnswer.objects.filter(attempt=attempt)
    total_score = sum(answer.score_awarded for answer in answers)
    
    penalty = Decimal('0.00')
    if attempt.is_late:
        penalty = (attempt.assessment.late_penalty_percent / Decimal('100')) * total_score
    
    final_score = total_score - penalty
    attempt.score = total_score
    attempt.penalty_applied = penalty
    attempt.final_score = final_score
    attempt.save()
       
        
def update_assessment_result(assessment, student_id):
    attempts = AssessmentAttempt.objects.filter(
        assessment_id=assessment, student_id=student_id
    )

    if not attempts.exists():
        return

    policy = assessment.scoring_policy
    result, _ = AssessmentResult.objects.get_or_create(
        assessment_id=assessment,
        student_id=student_id,
        defaults={'final_score': Decimal('0.00'), 'policy_used': policy, 'attempt_id': attempts.last()}
    )

    if policy == 'highest':
        best = attempts.order_by('-final_score').first()
        result.final_score = best.final_score
        result.attempt_id = best
    elif policy == 'latest':
        latest = attempts.order_by('-created_at').first()
        result.final_score = latest.final_score
        result.attempt_id = latest
    elif policy == 'average':
        avg = attempts.aggregate(avg=models.Avg('final_score'))['avg'] or Decimal('0.00')
        result.final_score = avg
        result.attempt_id = attempts.order_by('-created_at').first()
    elif policy == 'first':
        first = attempts.order_by('created_at').first()
        result.final_score = first.final_score
        result.attempt_id = first

    result.policy_used = policy
    result.save()

# POST /api/assessment_answers/{id}/grade/
# Grade essay answers with validation

# GET /api/assessment_answers/ungraded/?assessment_id=5
# Get all pending answers for an assessment

# GET /api/assessment_answers/attempt-answers/?attempt_id=42
# View all answers for a specific attempt