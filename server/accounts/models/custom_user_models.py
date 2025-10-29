from django.db import models
from django.contrib.auth.models import AbstractUser
from cuid import cuid

class CustomUser(AbstractUser):
    cuid = models.CharField(primary_key=True, default=cuid, editable=False, max_length=36)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null = True, blank=True, auto_now_add=True)
    otp_attempts = models.IntegerField(default=0)
    failed_otp_count = models.IntegerField(default=0)
    failed_login_count = models.IntegerField(default=0)
    otp_blocked_until = models.DateTimeField(null=True, blank=True) 
    account_locked_permanent = models.BooleanField(default=False)

    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def has_perm(self, perm, obj=None):
        if super().has_perm(perm, obj):
            return True

        if hasattr(self, 'profile') and self.profile.role:
            role_permissions = self.profile.role.permissions.all()
            if role_permissions.filter(codename=perm.split('.')[1]).exists():
                return True
        
        return False
