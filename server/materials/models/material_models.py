from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=255)
    subject_id = models.ForeignKey('teachingload.Subject', on_delete=models.PROTECT)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT)
    is_hidden = models.BooleanField(default=False)
    grading_period_id = models.ForeignKey('academicrecord.GradingPeriod', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
        