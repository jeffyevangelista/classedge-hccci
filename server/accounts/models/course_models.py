from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    