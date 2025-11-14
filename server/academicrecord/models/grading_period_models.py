from django.db import models

class GradingPeriod(models.Model):
    grading_period_category_id = models.ForeignKey('GradingPeriodCategory', on_delete=models.CASCADE)
    academic_term_id = models.ForeignKey('AcademicTerm', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.academic_term_id} - {self.grading_period_category_id.name}"

    class Meta:
        unique_together = ('academic_term_id', 'grading_period_category_id')
