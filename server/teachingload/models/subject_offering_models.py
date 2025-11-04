from django.db import models
from django.conf import settings

class SubjectOffering(models.Model):
    subject_id = models.ForeignKey('Subject', on_delete=models.PROTECT,null=True,blank=True)
    teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_subject_offerings', on_delete=models.PROTECT,null=True,blank=True)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborator', blank=True)
    semester_id = models.ForeignKey('academicrecord.Semester', on_delete=models.PROTECT,null=True,blank=True)
    max_enrollee = models.IntegerField()
    current_enrollee = models.IntegerField()
    duration_start = models.DateField()
    duration_end = models.DateField()
    
    def __str__(self):
        collaborators = ", ".join([str(c) for c in self.collaborators.all()]) if self.collaborators.exists() else "No collaborators"
        return f"{self.subject_id} - {self.semester_id} - {self.teacher_id} ({collaborators})"
