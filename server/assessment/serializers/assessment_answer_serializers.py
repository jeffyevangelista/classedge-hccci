from rest_framework import serializers
from assessment.models import AssessmentAnswer

class AssessmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAnswer
        fields = '__all__'
