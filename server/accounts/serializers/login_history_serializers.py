from rest_framework import serializers
from accounts.models import LoginHistory

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__'