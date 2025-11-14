from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicYearSerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from common.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class AcademicYearViewSet(ModelViewSet):
    serializer_class = AcademicYearSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'start_date', 'end_date']
    search_fields = ['name', 'start_date', 'end_date']
    ordering_fields = ['name', 'start_date', 'end_date']
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')

    # Non-paginated endpoint: /api/academic-years/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
