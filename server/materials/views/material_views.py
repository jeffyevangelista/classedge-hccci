from rest_framework.viewsets import ModelViewSet
from materials.serializers import MaterialSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination

class MaterialViewSet(ModelViewSet):
    serializer_class = MaterialSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()