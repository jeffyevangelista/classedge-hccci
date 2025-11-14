from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from common.redis_client import redis_client
import uuid

User = get_user_model()

class LoginAndSendOTPView(APIView):
    """
    Combined login endpoint:
    1. Authenticate user credentials.
    2. Send OTP to user.
    3. Return otp_token for OTP verification.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=400)

        # --- Authenticate user ---
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or password."}, status=400)

        if not user.check_password(password):
            user.failed_login_count += 1
            user.save(update_fields=["failed_login_count"])
            return Response({"detail": "Invalid credentials."}, status=400)

        # --- Send OTP ---
        try:
            user.send_otp()  # This should email or SMS the OTP to the user
        except Exception as e:
            return Response({"detail": f"Failed to send OTP: {str(e)}"}, status=500)

        # --- Store OTP token in Redis ---
        otp_token = str(uuid.uuid4())
        redis_client.setex(f"otp:{otp_token}", 600, user.cuid)  # TTL 10 minutes

        return Response(
            {"otp_token": otp_token, "detail": "OTP sent successfully. Please check your email."},
            status=200
        )
