from rest_framework.viewsets import ModelViewSet
from accounts.serializers import DisplayImageSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class DisplayImageViewSet(ModelViewSet):
    serializer_class = DisplayImageSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
