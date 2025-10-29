from rest_framework import serializers
from assessment.models import AssessmentQuestion

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = '__all__'