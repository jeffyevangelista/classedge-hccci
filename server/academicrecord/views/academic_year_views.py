from rest_framework.viewsets import ModelViewSet
from academicrecord.serializers import AcademicYearSerializer    
from rest_framework.authentication import SessionAuthentication
from accounts.utils import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class AcademicYearViewSet(ModelViewSet):
    serializer_class = AcademicYearSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().order_by('-created_at')


class GenericAcademicYearViewSet(GenericAPIView):
    serializer_class = AcademicYearSerializer
    authentication_classes = [SessionAuthentication, CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get(self, request):
        return Response(self.serializer_class(self.serializer_class.Meta.model.objects.all().order_by('-created_at')).data)