from rest_framework import serializers
from academicrecord.models import GradingPeriod  

class GradingPeriodSerializer(serializers.ModelSerializer):
    academic_term = serializers.CharField(source='academic_term_id.name', read_only=True)
    grading_period_category = serializers.CharField(source='grading_period_category_id.name', read_only=True)

    class Meta:
        model = GradingPeriod
        fields = '__all__'
