from django.urls import path,include
from rest_framework.routers import DefaultRouter
from accounts.utils import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieLogoutView,
)
from accounts.views import *
from accounts.utils import *

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'display-images', DisplayImageViewSet, basename='display-image')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'certificates', CertificateViewSet, basename='certificate')


urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),

            # Auth endpoints
            path("auth/send-otp/", LoginAndSendOTPView.as_view(), name="send_otp"),
            path("auth/verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
            path("auth/login/",   CookieTokenObtainPairView.as_view(), name="jwt-login"),
            path("auth/refresh/", CookieTokenRefreshView.as_view(),    name="jwt-refresh"),
            path("auth/logout/",  CookieLogoutView.as_view(),          name="jwt-logout"),

            # Other custom endpoints
            path("microsoft/login/", oauth2_login, name="microsoft_login"),
            path("microsoft/login/callback/", oauth2_callback, name="microsoft_callback"),
            path("login-history/", LoginHistoryViewSet.as_view(), name="login-history"),

        ])
    ),
    

]
