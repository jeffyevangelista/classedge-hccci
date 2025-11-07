from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_enrollments', on_delete=models.PROTECT)
    subject_offer_id = models.ForeignKey('teachingload.SubjectOffering', related_name='teacher_subject_offerings', on_delete=models.PROTECT, null=True, blank=True)
    academic_term_id = models.ForeignKey('AcademicTerm', related_name='academic_term_enrollments', on_delete=models.PROTECT, null=True, blank=True)
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
        return f"{self.student_id} - {self.subject_offer_id} - {self.academic_term_id} - {self.enrollment_date} - {self.status}"

    class Meta:
        unique_together = ('student_id', 'subject_offer_id', 'academic_term_id')

