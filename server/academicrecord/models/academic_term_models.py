from django.db import models

class AcademicTerm(models.Model):
    academic_year_id = models.ForeignKey('AcademicYear', on_delete=models.PROTECT)
    academic_term_category_id = models.ForeignKey('AcademicTermCategory', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    calculation_method = models.CharField(max_length=50,choices=[('Averaging', 'Averaging'), ('Term Percentage', 'Term Percentage')], default='averaging')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.academic_year_id} - {self.academic_term_category_id.name}"

    class Meta:
        unique_together = ('academic_year_id', 'academic_term_category_id')

