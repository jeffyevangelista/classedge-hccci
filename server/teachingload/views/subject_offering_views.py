from rest_framework import viewsets
from teachingload.serializers import SubjectOfferingSerializer
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class SubjectOfferingViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectOfferingSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')

    # Non-paginated endpoint: /api/subject-offerings/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)