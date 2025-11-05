from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction

class TermWeight(models.Model):
    grading_period_id = models.ForeignKey('academicrecord.GradingPeriod', on_delete=models.CASCADE)
    subjects_id = models.ManyToManyField('teachingload.Subject', related_name='term_weights')
    base_grade = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_by_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.grading_period_id.name

    # Get all existing weights for same term and same semester
    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            for subject in self.subjects_id.all():
                total = (
                    TermWeight.objects
                    .filter(grading_period_id=self.grading_period_id, subjects_id=subject)
                    .aggregate(models.Sum('percentage'))['percentage__sum'] or 0
                )
                if total > 100:
                    raise ValidationError(
                        f"Total term weight for {subject.name} in {self.grading_period_id.name} exceeds 100%."
                    )
