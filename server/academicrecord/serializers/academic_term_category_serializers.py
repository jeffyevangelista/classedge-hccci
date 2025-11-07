from rest_framework import serializers
from academicrecord.models import AcademicTermCategory

class AcademicTermCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTermCategory
        fields = '__all__'
