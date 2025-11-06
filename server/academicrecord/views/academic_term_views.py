from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicTermSerializer   
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class AcademicTermViewSet(ModelViewSet):
    serializer_class = AcademicTermSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['academic_year_id', 'academic_term_category_id']
    search_fields = ['academic_year_id', 'academic_term_category_id']
    ordering_fields = ['academic_year_id', 'academic_term_category_id', 'start_date', 'end_date']


    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')

    # Non-paginated endpoint: /api/academic-terms/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
