from django.db import models
from django.core.exceptions import ValidationError

class ComponentWeight(models.Model):
    gradebook = models.ForeignKey('Gradebook', on_delete=models.PROTECT)
    assessment_type = models.ForeignKey('assessment.AssessmentType', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name="subcomponents")
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        parent_str = f"{self.parent.assessment_type.name} → " if self.parent else ""
        return f"{parent_str}{self.assessment_type.name} ({self.percentage}%)"

    def clean(self):
        if self.parent:
            siblings = ComponentWeight.objects.filter(parent=self.parent).exclude(pk=self.pk)
            total = sum(s.percentage for s in siblings) + self.percentage
            if total > 100:
                raise ValidationError("Total percentage of subcomponents exceeds 100%.")
        else:
            siblings = ComponentWeight.objects.filter(gradebook=self.gradebook, parent__isnull=True).exclude(pk=self.pk)
            total = sum(s.percentage for s in siblings) + self.percentage
            if total > 100:
                raise ValidationError("Total percentage of top-level components exceeds 100% in this gradebook.")



    