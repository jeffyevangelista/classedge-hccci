from rest_framework import serializers
from teachingload.models import ScheduleType

class ScheduleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = '__all__'
