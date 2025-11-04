from django.db import models
from django.core.exceptions import ValidationError

class ComponentWeight(models.Model):
    gradebook_id = models.ForeignKey('Gradebook', on_delete=models.PROTECT)
    assessment_type_id = models.ForeignKey('assessment.AssessmentType', on_delete=models.PROTECT)
    parent_id = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name="subcomponents")
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        parent_str = f"{self.parent_id.assessment_type.name} → " if self.parent_id else ""
        return f"{parent_str}{self.assessment_type.name} ({self.percentage}%)"

    def clean(self):
        if self.parent_id:
            siblings = ComponentWeight.objects.filter(parent_id=self.parent_id).exclude(pk=self.pk)
            total = sum(s.percentage for s in siblings) + self.percentage
            if total > 100:
                raise ValidationError("Total percentage of subcomponents exceeds 100%.")
        else:
            siblings = ComponentWeight.objects.filter(gradebook_id=self.gradebook_id, parent_id__isnull=True).exclude(pk=self.pk)
            total = sum(s.percentage for s in siblings) + self.percentage
            if total > 100:
                raise ValidationError("Total percentage of top-level components exceeds 100% in this gradebook.")


    