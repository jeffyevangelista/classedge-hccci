from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import GradingPeriodSerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class GradingPeriodViewSet(ModelViewSet):
    serializer_class = GradingPeriodSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['grading_period_category_id', 'academic_term_id']
    search_fields = ['grading_period_category_id__name', 'academic_term_id__name', 'start_date', 'end_date']
    ordering_fields = ['grading_period_category_id', 'academic_term_id', 'start_date', 'end_date']
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    # Non-paginated endpoint: /api/grading-periods/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
