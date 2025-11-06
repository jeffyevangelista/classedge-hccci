from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicTermSerializer   
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class AcademicTermViewSet(ModelViewSet):
    serializer_class = AcademicTermSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')

    # Non-paginated endpoint: /api/academic-terms/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
