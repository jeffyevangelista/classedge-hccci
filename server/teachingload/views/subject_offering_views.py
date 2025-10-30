from rest_framework import viewsets
from teachingload.serializers import SubjectOfferingSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class SubjectOfferingViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectOfferingSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')