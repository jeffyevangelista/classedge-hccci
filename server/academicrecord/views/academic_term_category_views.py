from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicTermCategorySerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class AcademicTermCategoryViewSet(ModelViewSet):
    serializer_class = AcademicTermCategorySerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')
