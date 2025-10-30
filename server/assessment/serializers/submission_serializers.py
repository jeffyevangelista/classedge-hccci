from rest_framework import serializers
from assessment.models import SubmissionType

class SubmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionType
        fields = '__all__'