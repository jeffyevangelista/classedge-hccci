from rest_framework import serializers
from gradebook.models import ComponentWeight

class ComponentWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentWeight
        fields = '__all__'