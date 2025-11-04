from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AcademicYear)
admin.site.register(Semester)
admin.site.register(SemesterCategory)
admin.site.register(Term)
admin.site.register(TermCategory)
admin.site.register(Enrollment)
