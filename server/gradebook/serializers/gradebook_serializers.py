from rest_framework import serializers
from gradebook.models import Gradebook

class GradebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gradebook
        fields = '__all__'