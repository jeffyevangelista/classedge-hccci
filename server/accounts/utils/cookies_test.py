# cookies.py
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout as django_logout, get_user_model


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings


from django.conf import settings
from accounts.models import Profile, LoginHistory
from django.utils import timezone
from datetime import timedelta
import requests


User = get_user_model()



# --------------------------
# COOKIE CONFIG
# --------------------------
def cookie_opts(max_age: int):
    is_production = not settings.DEBUG
    return {
        "httponly": True,
        "secure": is_production,  # Only secure when HTTPS
        "samesite": "None" if is_production else "Lax",  # Cross-domain in production
        "path": "/",
        "max_age": max_age,
    }


    
# --------------------------
# CUSTOM TOKEN SERIALIZERS
# --------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """LOGIN: include nested user info with role inside access token."""


    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Handle user → profile → role relationship
        try:
            profile = user.profile
            role_name = profile.role.name if profile and profile.role else None
        except Profile.DoesNotExist:
            role_name = None


        token["role"] = [role_name] if role_name else []
        return token



class MinimalTokenRefreshSerializer(TokenRefreshSerializer):
    """REFRESH: return a minimal access token, ensure user still exists."""


    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])


        try:
            user_id = refresh[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise TokenError("Invalid refresh token: missing user id")


        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise TokenError("User not found")


        # Build new access token
        access = AccessToken.for_user(user)
        try:
            profile = user.profile
            role_name = profile.role.name if profile and profile.role else None
        except Profile.DoesNotExist:
            role_name = None


        access["role"] = [role_name] if role_name else []


        data = {"access": str(access)}


        # Optional rotation
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except Exception:
                    pass
            new_refresh = MinimalRefreshToken.for_user(user)
            data["refresh"] = str(new_refresh)


        return data



class MinimalRefreshToken(RefreshToken):
    """Custom minimal refresh token containing only user id + role."""


    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        try:
            profile = user.profile
            role_name = profile.role.name if profile and profile.role else None
        except Profile.DoesNotExist:
            role_name = None


        token["user"] = {
            "id": str(user.pk),
        }
        token["role"] = [role_name] if role_name else []


        # Strip out any unnecessary claims
        allowed = {
            "token_type",
            "exp",
            "iat",
            "jti",
            api_settings.USER_ID_CLAIM,
            "user",
        }
        for key in list(token.payload.keys()):
            if key not in allowed:
                del token.payload[key]
        return token



# --------------------------
# AUTH VIEWS
# --------------------------
class CookieTokenObtainPairView(TokenObtainPairView):
    """POST {username, password, recaptcha_token} → returns access JSON and sets refresh cookie."""


    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


    def verify_recaptcha(self, token):
        """Verify Google reCAPTCHA v2/v3."""
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": token,
        }
        try:
            r = requests.post(url, data=data, timeout=5)
            result = r.json()
        except Exception:
            return False, "Error contacting reCAPTCHA service."


        if not result.get("success"):
            return False, "Invalid reCAPTCHA. Please try again."


        score = result.get("score")
        if score is not None and score < settings.RECAPTCHA_REQUIRED_SCORE:
            return False, f"Low reCAPTCHA score ({score})."


        return True, None


    def post(self, request, *args, **kwargs):
        # recaptcha_token = request.data.get("recaptcha")
        # if not recaptcha_token:
        #     return Response({"detail": "Missing reCAPTCHA token."}, status=400)


        # # Always verify against Google's API
        # valid, err = self.verify_recaptcha(recaptcha_token)
        # if not valid:
        #     return JsonResponse({"error": err}, status=400)


        # Validate user credentials (authenticates the user)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])


        user = serializer.user


        # --- Require OTP verification within TTL ---
        OTP_VERIFIED_TTL = getattr(settings, "OTP_VERIFIED_TTL_MINUTES", 10)
        if not getattr(user, "otp_verified_at", None):
            return Response({"detail": "OTP not verified. Please verify OTP first."}, status=400)


        if timezone.now() - user.otp_verified_at > timedelta(minutes=OTP_VERIFIED_TTL):
            return Response({"detail": "OTP verification expired. Please request a new OTP."}, status=400)


        # Reset OTP verification flag (prevent reuse)
        user.otp_verified_at = None
        user.save(update_fields=["otp_verified_at"])


        # Generate tokens
        access = str(serializer.validated_data["access"])
        refresh = str(MinimalRefreshToken.for_user(user))


        # Record login history
        LoginHistory.objects.create(user=user)


        # Build secure cookie response
        resp = JsonResponse({"access": access}, status=status.HTTP_200_OK)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"


        access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())


        resp.set_cookie("access", access, **cookie_opts(access_max_age))
        resp.set_cookie("refresh", refresh, **cookie_opts(refresh_max_age))
        return resp




class CookieTokenRefreshView(TokenRefreshView):
    """GET or POST → refresh access token using the refresh cookie."""


    permission_classes = [AllowAny]
    serializer_class = MinimalTokenRefreshSerializer
    http_method_names = ["get", "post", "head", "options"]


    def _refresh_from_cookie(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"detail": "No refresh cookie found."}, status=status.HTTP_401_UNAUTHORIZED)


        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)


        access = serializer.validated_data["access"]
        resp = JsonResponse({"access": access}, status=status.HTTP_200_OK)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"


        # Reset access cookie
        access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        resp.set_cookie("access", access, **cookie_opts(access_max_age))


        # Handle refresh rotation (optional)
        if "refresh" in serializer.validated_data:
            new_refresh = serializer.validated_data["refresh"]
            refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
            resp.set_cookie("refresh", new_refresh, **cookie_opts(refresh_max_age))


        # Renew CSRF token
        resp.set_cookie(
            settings.CSRF_COOKIE_NAME,
            get_token(request),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            path="/",
        )


        return resp


    def get(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)


    def post(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)



class CookieLogoutView(APIView):
    """Logs user out and clears cookies."""


    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass


        django_logout(request)
        resp = JsonResponse({"message": "Logged out"})
        for name in ("access","refresh", settings.CSRF_COOKIE_NAME):
            resp.delete_cookie(name, path="/")
        return resp

