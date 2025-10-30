from django.db import models

class Term(models.Model):
    term_category = models.ForeignKey('TermCategory', on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.semester.name} - {self.term_category.name}"

    class Meta:
        unique_together = ('semester', 'term_category')
