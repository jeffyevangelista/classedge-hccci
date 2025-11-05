from rest_framework import serializers
from teachingload.models import SubjectOffering

class SubjectOfferingSerializer(serializers.ModelSerializer):
    schedule = serializers.CharField(source='schedule_id.name', read_only=True)
    subject = serializers.CharField(source='subject_id.name', read_only=True)
    academic_term = serializers.CharField(source='academic_term_id.name', read_only=True)
    teacher = serializers.CharField(source='teacher_id.name', read_only=True)
    collaborators = serializers.CharField(source='collaborators.name', read_only=True)

    class Meta:
        model = SubjectOffering
        fields = '__all__'
