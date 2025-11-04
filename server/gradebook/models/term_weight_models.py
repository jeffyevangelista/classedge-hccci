from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction

class TermWeight(models.Model):
    term_id = models.ForeignKey('academicrecord.Term', on_delete=models.CASCADE)
    subjects_id = models.ManyToManyField('teachingload.Subject', related_name='term_weights')
    base_grade = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_by_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.term_id.name

    # Get all existing weights for same term and same semester
    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            for subject in self.subjects_id.all():
                total = (
                    TermWeight.objects
                    .filter(term__semester=self.term_id.semester, subjects_id=subject)
                    .aggregate(models.Sum('percentage'))['percentage__sum'] or 0
                )
                if total > 100:
                    raise ValidationError(
                        f"Total term weight for {subject.name} in {self.term_id.semester.name} exceeds 100%."
                    )


