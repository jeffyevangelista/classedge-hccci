from django.db import models
from django.contrib.auth.models import AbstractUser
from cuid import cuid
from django.conf import settings
import random
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

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
    otp_verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def generate_otp(self):
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = timezone.now()
        self.otp_verified_at = None
        self.otp_attempts = 0
        self.save(update_fields=["otp", "otp_created_at", "otp_verified_at", "otp_attempts"])

    def send_otp(self):
        self.generate_otp()
        message = f"""Hi there,

We received a request to login for your Classedge account.

🔐 Your OTP code: {self.otp}

This code will expire in 5 minutes and can only be used once.

Security Notice:
If you didn't request this login, please ignore this message or contact our support team immediately.

— The Classify Team"""
        send_mail(
            subject="Your Login OTP",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False,
        )

    def is_otp_valid(self, otp):
        if not self.otp or not self.otp_created_at:
            return False
        if timezone.now() - self.otp_created_at > timedelta(minutes=5):
            return False
        return str(self.otp) == str(otp)

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

