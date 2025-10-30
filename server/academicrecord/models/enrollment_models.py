from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_enrollments', on_delete=models.PROTECT)
    subject_offering = models.ForeignKey('teachingload.SubjectOffering', related_name='teacher_subject_offerings', on_delete=models.PROTECT, null=True, blank=True)
    semester = models.ForeignKey('Semester', related_name='semester_enrollments', on_delete=models.PROTECT, null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enrolled') 
    drop_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student} - {self.subject_offering} - {self.semester} - {self.enrollment_date} - {self.status}"

    class Meta:
        unique_together = ('student', 'subject_offering', 'semester')

