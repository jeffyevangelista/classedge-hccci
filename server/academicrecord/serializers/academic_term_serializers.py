from rest_framework import serializers
from academicrecord.models import AcademicTerm

class AcademicTermSerializer(serializers.ModelSerializer):
    academic_year = serializers.CharField(source='academic_year_id.name',read_only=True)
    academic_term_category = serializers.CharField(source='academic_term_category_id.name',read_only=True)

    class Meta:
        model = AcademicTerm
        fields = '__all__'
