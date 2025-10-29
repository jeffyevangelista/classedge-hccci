from rest_framework import serializers
from assessment.models import AssessmentType

class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = '__all__'