from rest_framework.viewsets import ModelViewSet
from assessment.serializers import AssessmentTypeSerializer
from common.pagination import CustomPagination
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class AssessmentTypeViewSet(ModelViewSet):
    serializer_class = AssessmentTypeSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()