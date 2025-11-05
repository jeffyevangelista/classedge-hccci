from rest_framework import serializers
from academicrecord.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    academic_term = serializers.CharField(source='academic_term_id.name')
    subject_offering = serializers.CharField(source='subject_offering_id.name')
    student = serializers.CharField(source='student_id.name')

    class Meta:
        model = Enrollment
        fields = '__all__'
