from django.db import models
import os
import uuid
from django.utils.timezone import now

def get_upload_path_badge(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'badges/{uuid.uuid4()}{ext}'

class Badge(models.Model):
    profiles = models.ManyToManyField('Profile', related_name='badges')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_upload_path_badge)
    description = models.TextField(null=True, blank=True)
    date_awarded = models.DateField(default=now)
    created_at = models.DateTimeField(default=now, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.pk:
            profile_names = ", ".join([f"{p.first_name} {p.last_name}" for p in self.profiles.all()])
            return f"{self.name} - {profile_names}"
        return self.name
