from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import SemesterSerializer   
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class SemesterViewSet(ModelViewSet):
    serializer_class = SemesterSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
