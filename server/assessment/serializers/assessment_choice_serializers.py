from rest_framework import serializers
from assessment.models import AssessmentChoice

class AssessmentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentChoice
        fields = '__all__'