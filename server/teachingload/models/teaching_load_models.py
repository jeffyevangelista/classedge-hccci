from django.db import models
import uuid
import os
from django.conf import settings

def get_upload_path_subject_photo(instance, filename):
    filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    return os.path.join('subject_photo', filename)

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    unit = models.IntegerField()
    photo = models.ImageField(upload_to=get_upload_path_subject_photo, blank=True, null=True)
    teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    collaborator = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborator', blank=True)
    is_coil = models.BooleanField(default=False)
    is_hali = models.BooleanField(default=False)
    color = models.CharField(max_length=255, blank=True, null=True)
    max_enrollee = models.IntegerField()
    current_enrollee = models.IntegerField()
    duration = models.CharField(max_length=255)
    partner_institution = models.CharField(max_length=255)
    target_sdgs = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.teacher}"
    
    