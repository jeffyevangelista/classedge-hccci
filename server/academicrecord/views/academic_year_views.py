from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicYearSerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class AcademicYearViewSet(ModelViewSet):
    serializer_class = AcademicYearSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')
