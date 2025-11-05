from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicTermCategorySerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.decorators import action

class AcademicTermCategoryViewSet(ModelViewSet):
    serializer_class = AcademicTermCategorySerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    # Non-paginated endpoint: /api/academic-term-categories/all/
    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
