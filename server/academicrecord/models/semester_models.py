from django.db import models

class Semester(models.Model):
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.PROTECT)
    semester_category = models.ForeignKey('SemesterCategory', on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    passing_grade = models.DecimalField(max_digits=5, decimal_places=2)
    calculation_method = models.CharField(max_length=50,choices=[('Averaging', 'Averaging'), ('Term Percentage', 'Term Percentage')], default='averaging')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.academic_year} - {self.semester_category.name}"

    class Meta:
        unique_together = ('academic_year', 'semester_category')

