from rest_framework import serializers
from assessment.models import AssessmentAttempt

class AssessmentAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAttempt
        fields = '__all__'
