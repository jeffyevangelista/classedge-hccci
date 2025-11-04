from django.db import models

class AssessmentChoice(models.Model):
    question_id = models.ForeignKey('AssessmentQuestion', on_delete=models.PROTECT, related_name='choices', null=True, blank=True)
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
def __str__(self):
    return self.choice_text