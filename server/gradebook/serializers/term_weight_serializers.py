from rest_framework import serializers
from gradebook.models import TermWeight

class TermWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermWeight
        fields = '__all__'