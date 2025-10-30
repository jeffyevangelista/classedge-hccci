from rest_framework import serializers
from teachingload.models import SubjectOffering

class SubjectOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectOffering
        fields = '__all__'
