from django.db import models
from systemlog.models import SystemLog

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            SystemLog.objects.create(
                user=self.created_by,
                action='Create',
                module='Department',
                entity_id=self.pk,
                description=f'Created department: {self.name}',
                ip_address=self.created_by.ip_address,
            )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
