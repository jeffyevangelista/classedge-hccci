from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AcademicYear)
admin.site.register(AcademicTerm)
admin.site.register(AcademicTermCategory)
admin.site.register(GradingPeriod)
admin.site.register(GradingPeriodCategory)
admin.site.register(Enrollment)
