from rest_framework.viewsets import ModelViewSet
from gradebook.serializers import TermWeightSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination

class TermWeightViewSet(ModelViewSet):
    serializer_class = TermWeightSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()