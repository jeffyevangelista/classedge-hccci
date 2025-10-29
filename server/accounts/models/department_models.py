from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
