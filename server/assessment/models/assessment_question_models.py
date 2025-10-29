from django.db import models
    
class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey('Assessment', on_delete=models.PROTECT, related_name='questions', null=True, blank=True)
    question_text = models.TextField()
    assessment_type = models.ForeignKey('AssessmentType', on_delete=models.PROTECT, related_name='questions', null=True, blank=True)
    points = models.DecimalField(max_digits=5, decimal_places=2)
    order_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.question_text