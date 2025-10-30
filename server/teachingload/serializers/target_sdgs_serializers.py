from rest_framework import serializers
from teachingload.models import SDG

class SDGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDG
        fields = '__all__'
