from rest_framework import serializers
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser, Profile
import re

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    badges = serializers.SerializerMethodField()
    certificates = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    department_id = serializers.IntegerField(source='department.id', read_only=True)
    course_id = serializers.IntegerField(source='course.id', read_only=True)
    permissions = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'permissions', 
            'password',
            'date_of_birth',
            'gender',
            'nationality',
            'address',
            'id_number',
            'phone_number',
            'photo',
            'status',
            'department_id',
            'department',
            'course_id',
            'course',
            'badges',
            'certificates',
            'grade_year_level',
        ]
        
        read_only_fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'id_number',
            'badges',
            'certificates',
        ]
        
    def validate_phone_number(self, value):
        """Validate phone number length and format"""
        if value:
            if not re.match(r'^(09|\+639)\d{9}$', value):
                raise serializers.ValidationError(
                    "Phone number must start with '09' or '+639' and contain 11 digits."
                )
        return value

    def get_role(self, instance):
        """Return role name as an array"""
        if instance.role:
            return [instance.role.name]
        return []
    
    def get_badges(self, instance):
        """Return list of badge names"""
        return [badge.name for badge in instance.badges.all()]
    
    def get_certificates(self, instance):
        """Return list of certificate titles"""
        return [cert.title for cert in instance.certificates.all()]
    
    def get_department(self, instance):
        """Return department name if assigned"""
        return instance.department.name if instance.department else None
    
    def get_course(self, instance):
        """Return course name if assigned"""
        return instance.course.name if instance.course else None

    def get_permissions(self, instance):
        """Return list of permission codenames from the role"""
        if instance.role:
            return [perm.codename for perm in instance.role.permissions.all()]
        return []

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password', None)

        # Separate user fields
        user_data = {
            'username': validated_data.get('email'),  # username = email
            'email': validated_data.get('email'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
        }
        user = CustomUser.objects.create_user(**user_data)
        if password:
            user.set_password(password)
            user.save()

        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update user password if provided
        if password:
            instance.user.set_password(password)
            instance.user.save()

        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # fetch related profile safely
        try:
            profile = user.profile
            role_name = profile.role.name if profile and profile.role else None
        except Profile.DoesNotExist:
            role_name = None

        token['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': role_name,
        }

        # remove unnecessary keys from payload
        for key in ('email', 'first_name', 'last_name', 'role'):
            token.pop(key, None)

        return token

