from rest_framework import serializers
from academicrecord.models import SemesterCategory

class SemesterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCategory
        fields = '__all__'
