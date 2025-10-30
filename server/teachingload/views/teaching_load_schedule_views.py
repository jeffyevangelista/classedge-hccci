from rest_framework.viewsets import ModelViewSet
from teachingload.serializers import ScheduleSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination

class ScheduleViewSet(ModelViewSet):
    serializer_class = ScheduleSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()