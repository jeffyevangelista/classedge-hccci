from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.PROTECT)
    subject = models.ForeignKey('teachingload.Subject', related_name='enrollments', on_delete=models.PROTECT)
    semester = models.ForeignKey('Semester', related_name='enrollments', on_delete=models.PROTECT)
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
        return f"{self.student} - {self.subject} - {self.semester} - {self.enrollment_date} - {self.status}"
