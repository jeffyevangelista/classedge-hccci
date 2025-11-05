from django.db import models
from django.conf import settings    

class AssessmentAnswer(models.Model):
    GRADING_STATUS_CHOICES = [
        ('auto_graded', 'Auto Graded'),
        ('pending_review', 'Pending Review'),
        ('graded', 'Graded'),
    ]
    
    attempt_id = models.ForeignKey('AssessmentAttempt', on_delete=models.PROTECT, related_name='answers', null=True, blank=True)
    question_id = models.ForeignKey('AssessmentQuestion', on_delete=models.PROTECT, related_name='answers', null=True, blank=True)
    assessment_choice_id = models.ForeignKey('AssessmentChoice', on_delete=models.PROTECT, related_name='answers', null=True, blank=True)
    answer_text = models.TextField(blank=True)
    score_awarded = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grading_status = models.CharField(max_length=20, choices=GRADING_STATUS_CHOICES, default='pending_review')
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='graded_answers',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Answer to {self.question} by {self.attempt.student}"