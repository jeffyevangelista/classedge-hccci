from rest_framework import serializers
from gradebook.models import GradebookCategory

class GradebookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GradebookCategory
        fields = '__all__'