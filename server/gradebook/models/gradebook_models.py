from django.db import models
from django.core.exceptions import ValidationError

class Gradebook(models.Model):
    gradebook_category_id = models.ForeignKey('GradebookCategory', on_delete=models.PROTECT)
    subject_offering_id = models.ForeignKey('teachingload.SubjectOffering', on_delete=models.PROTECT)
    grading_period_id = models.ForeignKey('academicrecord.GradingPeriod', on_delete=models.PROTECT, related_name='gradebooks')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.gradebook_category_id.name} - {self.subject_offering_id} - {self.grading_period_id}"

    class Meta:
        unique_together = ('subject_offering_id', 'grading_period_id', 'gradebook_category_id')

    def clean(self):
        total = (
            Gradebook.objects
            .filter(subject_offering_id=self.subject_offering_id, grading_period_id=self.grading_period_id)
            .exclude(pk=self.pk)
            .aggregate(models.Sum('percentage'))['percentage__sum'] or 0
        )
        if total + self.percentage > 100:
            raise ValidationError("Total gradebook percentage exceeds 100% for this subject and term.")

