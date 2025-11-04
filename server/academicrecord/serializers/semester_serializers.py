from rest_framework import serializers
from academicrecord.models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    academic_year = serializers.CharField(source='academic_year_id.name')
    semester_category = serializers.CharField(source='semester_category_id.name')

    class Meta:
        model = Semester
        fields = '__all__'
