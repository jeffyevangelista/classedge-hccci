from rest_framework import generics
from accounts.serializers import LoginHistorySerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination

class LoginHistoryViewSet(generics.ListAPIView):
    serializer_class = LoginHistorySerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
