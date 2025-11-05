from rest_framework import serializers
from academicrecord.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    academic_term = serializers.CharField(source='academic_term_id.name', read_only=True)
    subject_offering = serializers.CharField(source='subject_offering_id.name', read_only=True)
    student = serializers.CharField(source='student_id.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
