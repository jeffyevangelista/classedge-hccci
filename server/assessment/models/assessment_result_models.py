from django.db import models
from django.conf import settings    

class AssessmentResult(models.Model):
    assessment_id = models.ForeignKey('Assessment', on_delete=models.PROTECT, related_name='results', null=True, blank=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='results', null=True, blank=True)
    final_score = models.DecimalField(max_digits=5, decimal_places=2)
    attempt_id = models.ForeignKey('AssessmentAttempt', on_delete=models.PROTECT, related_name='results', null=True, blank=True)
    computed_at = models.DateTimeField(auto_now_add=True)
    policy_used = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student} - {self.assessment.title}"
