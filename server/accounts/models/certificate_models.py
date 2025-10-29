from django.db import models
import uuid
import os
from django.utils.timezone import now

def get_upload_path_certificate(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'certificate/{uuid.uuid4()}{ext}'

class Certificate(models.Model):
    profiles = models.ManyToManyField('Profile', related_name='certificates')
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to=get_upload_path_certificate)
    issued_date = models.DateField(default=now)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.pk:
            names = ", ".join([f"{p.first_name} {p.last_name}" for p in self.profiles.all()])
            return f"{self.title} - {names}"
        return self.title