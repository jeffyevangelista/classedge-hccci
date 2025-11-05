from rest_framework import serializers
from assessment.models import QuestionType

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'