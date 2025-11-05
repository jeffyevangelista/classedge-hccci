from rest_framework import serializers
from academicrecord.models import GradingPeriodCategory

class GradingPeriodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingPeriodCategory
        fields = '__all__'
