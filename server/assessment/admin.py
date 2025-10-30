from django.contrib import admin
from assessment.models import *

admin.site.register(Assessment)
admin.site.register(AssessmentQuestion)
admin.site.register(AssessmentChoice)
admin.site.register(AssessmentAttempt)
admin.site.register(AssessmentAnswer)
admin.site.register(AssessmentResult)
admin.site.register(AssessmentType)
admin.site.register(SubmissionType)
