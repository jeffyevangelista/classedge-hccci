# views_auth.py

from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout as django_logout, get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

def _cookie_opts(max_age: int, *, httponly: bool = True):
    return {
        "httponly": httponly,
        "secure": settings.SESSION_COOKIE_SECURE,
        "samesite": settings.SESSION_COOKIE_SAMESITE,
        "path": "/",
        "max_age": max_age,
    }

# ---------- SERIALIZERS ----------
# All user Details in Access Token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """LOGIN: include `roles` directly in access token."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        role = getattr(user, "role", None)
        token["roles"] = [role] if role else []
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            # already raised by DRF as {"detail": "..."} — rethrow cleanly
            raise AuthenticationFailed(detail="Incorrect email or password.")
        except Exception:
            # catch other errors (e.g., inactive user)
            raise AuthenticationFailed(detail="Incorrect email or password.")
        return data


class MinimalTokenRefreshSerializer(TokenRefreshSerializer):
    """
    REFRESH: Build minimal ACCESS from user_id; verify user exists.
    """
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

        access = AccessToken.for_user(user)
        role = getattr(user, "role", None)
        access["roles"] = [role] if role else []

        data = {"access": str(access)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except Exception:
                    pass
            new_refresh = MinimalRefreshToken.for_user(user)
            data["refresh"] = str(new_refresh)

        return data


# ---------- VIEWS ----------
# Selected User detials in Refresh Token
class MinimalRefreshToken(RefreshToken):
    """Custom refresh token with only essential claims."""
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        allowed_claims = {
            "token_type", "exp", "iat", "jti", api_settings.USER_ID_CLAIM
        }
        # Remove any other keys that might have been added
        for key in list(token.payload.keys()):
            if key not in allowed_claims:
                del token.payload[key]
        return token

# Saved data to cookies upon login
class CookieTokenObtainPairView(TokenObtainPairView):
    """POST {email, password} → JSON(access w/ user), Set-Cookie(refresh)."""
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = str(serializer.validated_data["access"])
        refresh = str(MinimalRefreshToken.for_user(serializer.user))

        resp = JsonResponse({"access": access}, status=status.HTTP_200_OK)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"

        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

        # ✅ Only set refresh (JWT) cookie, not access
        resp.set_cookie(
            "jwt",  # you can keep "refresh" if you prefer
            refresh,
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            max_age=refresh_max_age,
            path="/"
        )

        # Keep CSRF token
        resp.set_cookie(
            settings.CSRF_COOKIE_NAME,
            get_token(request),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            path="/",
        )
        return resp

# request access token via request
class CookieTokenRefreshView(TokenRefreshView):
    """GET/POST - Reads 'jwt' cookie, returns new access token JSON."""
    permission_classes = [AllowAny]
    serializer_class = MinimalTokenRefreshSerializer

    def _refresh_from_cookie(self, request):
        refresh_token = request.COOKIES.get("jwt")
        if not refresh_token:
            return Response({"detail": "No refresh cookie."}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        access = str(serializer.validated_data["access"])
        resp = JsonResponse({"access": access}, status=200)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"

        # If rotating, issue a new refresh cookie
        if "refresh" in serializer.validated_data:
            new_refresh = str(serializer.validated_data["refresh"])
            resp.set_cookie(
                "jwt",
                new_refresh,
                httponly=True,
                secure=settings.SESSION_COOKIE_SECURE,
                samesite=settings.SESSION_COOKIE_SAMESITE,
                path="/",
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
            )

        return resp

    def get(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)

    def post(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)


#clear access token upon logout
class CookieLogoutView(APIView):
    """POST — clears jwt cookie and optionally blacklists token."""
    def post(self, request):
        jwt_token = request.COOKIES.get("jwt")
        if jwt_token:
            try:
                RefreshToken(jwt_token).blacklist()
            except Exception:
                pass
        django_logout(request)
        resp = JsonResponse({"detail": "Logged out"}, status=200)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"
        resp.delete_cookie("jwt", path="/")
        return resp

