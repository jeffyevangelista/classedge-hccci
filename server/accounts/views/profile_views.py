from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from accounts.serializers import UserSerializer
from accounts.models import Profile
from accounts.utils import CookieJWTAuthentication
from accounts.utils import MicrosoftAuth2Adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from django.conf import settings
import requests
from django.http import JsonResponse
from accounts.models import CustomUser
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from common.pagination import CustomPagination
import base64
import hashlib
import os
from django.shortcuts import redirect

class ProfileViewSet(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        password = request.data.get('password', None)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if password:
            instance.user.set_password(password)
            instance.user.save()
            
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """GET = view your own profile, PATCH = update your own data"""
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        # PATCH (update)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")
    return code_verifier, code_challenge


def oauth2_login(request):
    """Redirect user to Microsoft login with PKCE"""
    code_verifier, code_challenge = generate_pkce()
    request.session["code_verifier"] = code_verifier

    auth_url = (
        f"https://login.microsoftonline.com/{settings.MS_TENANT_ID}/oauth2/v2.0/authorize"
        f"?client_id={settings.MS_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri=http://localhost:8000/api/microsoft/login/callback/"
        f"&response_mode=query"
        f"&scope=openid profile email User.Read"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    # 🔹 Instead of returning JSON, redirect the user to Microsoft’s login page
    return redirect(auth_url)


def oauth2_callback(request):
    """Handle Microsoft redirect and exchange code for tokens"""
    code = request.GET.get("code")
    print("CODE:", code)
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    code_verifier = request.session.get("code_verifier")
    print("CODE VERIFIER:", code_verifier)
    if not code_verifier:
        return JsonResponse({"error": "Missing code_verifier (PKCE)"}, status=400)

    token_url = f"https://login.microsoftonline.com/{settings.MS_TENANT_ID}/oauth2/v2.0/token"

    data = {
        "client_id": settings.MS_CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/api/microsoft/login/callback/",
        "code_verifier": code_verifier,
        "client_secret": settings.MS_CLIENT_SECRET,  # optional if using a public client
    }

    token_resp = requests.post(token_url, data=data)
    print("TOKEN RESPONSE:", token_resp.status_code, token_resp.text)
    token_data = token_resp.json()

    access_token = token_data.get("access_token")
    if not access_token:
        return JsonResponse({"error": "Failed to obtain Microsoft token"}, status=400)

    # --- Get user info from Microsoft Graph ---
    user_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_resp.json()
    email = user_info.get("mail") or user_info.get("userPrincipalName")

    user, _ = CustomUser.objects.get_or_create(
        email=email,
        defaults={
            "username": email.split("@")[0],
            "first_name": user_info.get("givenName", ""),
            "last_name": user_info.get("surname", "")
        }
    )

    SocialAccount.objects.update_or_create(
        user=user,
        provider="microsoft",
        defaults={"uid": user_info["id"], "extra_data": user_info}
    )

    # Log in and issue your own JWT tokens
    login(request, user)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    resp = JsonResponse({
        "message": "Microsoft login successful",
        "email": user.email,
    })

    # Set cookies for JWT
    access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

    resp.set_cookie("access", str(access), **cookie_opts(access_max_age))
    resp.set_cookie("refresh", str(refresh), **cookie_opts(refresh_max_age))

    resp.set_cookie(
        settings.CSRF_COOKIE_NAME,
        get_token(request),
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        path="/",
    )

    return resp

from django.http import JsonResponse

def test_session(request):
    if "counter" not in request.session:
        request.session["counter"] = 1
    else:
        request.session["counter"] += 1
    return JsonResponse({
        "counter": request.session["counter"],
        "session_key": request.session.session_key
    })



# Step 1: POST /auth/send-otp/ with { email, password } → show "OTP sent" if 200.

# Step 2: POST /auth/verify-otp-only/ with { email, otp } → on 200 show OTP verified.

# Step 3: POST /auth/login/ with { email, password, recaptcha_token } → receives access +

