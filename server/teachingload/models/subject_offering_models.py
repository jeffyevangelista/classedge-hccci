from django.db import models
from django.conf import settings

class SubjectOffering(models.Model):
    subject_id = models.ForeignKey('Subject', on_delete=models.PROTECT,null=True,blank=True)
    teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_subject_offerings', on_delete=models.PROTECT,null=True,blank=True)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborator', blank=True)
    academic_term_id = models.ForeignKey('academicrecord.AcademicTerm', on_delete=models.PROTECT,null=True,blank=True)
    schedule_id = models.ForeignKey('Schedule', on_delete=models.PROTECT,null=True,blank=True)
    max_enrollee = models.IntegerField(null=True, blank=True)
    current_enrollee = models.IntegerField(null=True, blank=True)
    duration_start = models.DateField(null=True, blank=True)
    duration_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        collaborators = ", ".join([str(c) for c in self.collaborators.all()]) if self.collaborators.exists() else "No collaborators"
        return f"{self.subject_id} - {self.academic_term_id} - {self.teacher_id} ({collaborators})"
