from rest_framework import serializers
from assessment.models import AssessmentResult

class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = '__all__'