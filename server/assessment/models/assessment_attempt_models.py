from django.db import models
from django.conf import settings    

# Student Record
class AssessmentAttempt(models.Model):
    assessment = models.ForeignKey('Assessment', on_delete=models.PROTECT, related_name='attempts', null=True, blank=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='attempts', null=True, blank=True)
    attempt_number = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    penalty_applied = models.DecimalField(max_digits=5, decimal_places=2)
    final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank =True)
        
    def __str__(self):
        return f"{self.student} - {self.assessment.title} - Attempt {self.attempt_number}"
