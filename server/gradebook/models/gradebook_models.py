from django.db import models
from django.core.exceptions import ValidationError

class Gradebook(models.Model):
    gradebook_category = models.ForeignKey('GradebookCategory', on_delete=models.PROTECT)
    subject_offering = models.ForeignKey('teachingload.SubjectOffering', on_delete=models.PROTECT)
    term = models.ForeignKey('academicrecord.Term', on_delete=models.PROTECT, related_name='gradebooks')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.gradebook_category.name} - {self.subject_offering} - {self.term}"

    class Meta:
        unique_together = ('subject_offering', 'term', 'gradebook_category')

    def clean(self):
        total = (
            Gradebook.objects
            .filter(subject_offering=self.subject_offering, term=self.term)
            .exclude(pk=self.pk)
            .aggregate(models.Sum('percentage'))['percentage__sum'] or 0
        )
        if total + self.percentage > 100:
            raise ValidationError("Total gradebook percentage exceeds 100% for this subject and term.")

