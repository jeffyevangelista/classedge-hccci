from rest_framework import serializers
from accounts.models import CustomUser, Role, Profile
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "content_type"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), 
        many=True, 
        write_only=True,
        source='permissions'
    )

    class Meta:
        model = Role
        fields = ["id", "name", "permissions", "permission_ids"]
        
    def validate_name(self, value):
        qs = Role.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Role name must be unique.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "photo", "role"]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "profile"]
