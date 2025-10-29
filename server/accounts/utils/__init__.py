from .auth import CookieJWTAuthentication
from .cookies import CookieTokenObtainPairView,CookieTokenRefreshView,CookieLogoutView
from .adapters import CustomAccountAdapter, CustomSocialAccountAdapter, MicrosoftAuth2Adapter
from .providers import MicrosoftAccount, MicrosoftProvider
from .send_otp import LoginAndSendOTPView
from .verify_otp import VerifyOTPView

__all__ = [
            # Auth
            'CookieJWTAuthentication',
            
            # Cookies
            'CookieTokenObtainPairView',
            'CookieTokenRefreshView',
            'CookieLogoutView',
            
            # Adapters
            'CustomAccountAdapter',
            'CustomSocialAccountAdapter',
            'MicrosoftAuth2Adapter',
            
            # Providers
            'MicrosoftAccount',
            'MicrosoftProvider',
            
            # OTP
            'LoginAndSendOTPView',
            'VerifyOTPView',
            
        ]









