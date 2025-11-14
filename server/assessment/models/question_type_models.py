from django.db import models

class QuestionType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    