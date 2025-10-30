from rest_framework import serializers
from academicrecord.models import TermCategory

class TermCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TermCategory
        fields = '__all__'
