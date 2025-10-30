from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from common.redis_client import redis_client

User = get_user_model()

class VerifyOTPView(APIView):
    """
    Verify OTP and issue JWT tokens (access + refresh).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        otp_token = request.data.get("otp_token")
        otp = request.data.get("otp")

        if not otp_token or not otp:
            return Response({"detail": "otp_token and otp are required."}, status=400)

        # --- Get user ID from Redis ---
        user_cuid = redis_client.get(f"otp:{otp_token}")
        if not user_cuid:
            return Response({"detail": "Invalid or expired OTP token."}, status=400)

        # --- Fetch user ---
        try:
            user = User.objects.get(cuid=user_cuid.decode())
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        # --- Verify OTP ---
        if not user.verify_otp(otp):  # Make sure your User model has verify_otp method
            return Response({"detail": "Invalid OTP."}, status=400)

        # --- OTP verified, delete OTP token ---
        redis_client.delete(f"otp:{otp_token}")

        # --- Issue JWT tokens ---
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Optional: store refresh token in HttpOnly cookie
        response = Response(
            {
                "detail": "OTP verified successfully.",
                "access": access_token,
                "refresh": refresh_token,
            },
            status=200
        )
        # Example of setting cookie:
        # response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")

        return response
