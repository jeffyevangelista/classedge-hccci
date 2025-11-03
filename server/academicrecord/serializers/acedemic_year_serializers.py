from rest_framework import serializers
from academicrecord.models import AcademicYear

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

    def validate_start_date(self, value):
        if not value:
            raise serializers.ValidationError("Start date must not be empty.")
        return value
    
    def validate_end_date(self, value):
        if not value:
            raise serializers.ValidationError("End date must not be empty.")
        return value
    