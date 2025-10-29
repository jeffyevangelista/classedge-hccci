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
from accounts.utils.cookies import cookie_opts
from common.pagination import CustomPagination

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
    

def oauth2_login(request):
    return OAuth2LoginView.adapter_view(MicrosoftAuth2Adapter)(request)


def oauth2_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    token_url = f"https://login.microsoftonline.com/{settings.MS_TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": settings.MS_CLIENT_ID,
        "client_secret": settings.MS_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/api/microsoft/login/callback/",
        
    }
    token_resp = requests.post(token_url, data=data)
    print("TOKEN RESPONSE:", token_resp.status_code, token_resp.text)
    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return JsonResponse({"error": "Failed to obtain Microsoft token"}, status=400)

    # Fetch Microsoft user profile
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

    # Link to SocialAccount
    SocialAccount.objects.update_or_create(
        user=user,
        provider='microsoft',
        defaults={"uid": user_info["id"], "extra_data": user_info}
    )

    # Log the user in (creates Django session)
    login(request, user)

    # Generate Django JWT tokens (SimpleJWT)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # Build response
    resp = JsonResponse({
        "message": "Microsoft login successful",
        "email": user.email,
    })

    # --- Set JWT cookies (for cookie-based auth flow) ---
    access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

    resp.set_cookie("access", str(access), **cookie_opts(access_max_age))
    resp.set_cookie("refresh", str(refresh), **cookie_opts(refresh_max_age))

    # --- Set CSRF cookie ---
    resp.set_cookie(
        settings.CSRF_COOKIE_NAME,
        get_token(request),
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        path="/",
    )

    return resp

