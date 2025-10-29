from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp, purpose='password reset', expiry_minutes=10):
    """Send OTP email with consistent formatting."""
    subject = f"🔐 Classedge {purpose.title()} OTP Code"
    
    message = f"""Hi there,

        We received a request to {purpose} for your Classedge account.

        🔐 Your OTP code: {otp}

        This code will expire in {expiry_minutes} minutes and can only be used once.

        Security Notice:
        If you didn't request this {purpose}, please ignore this message or contact our support team immediately.

        — The Classify Team"""
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
