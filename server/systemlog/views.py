from rest_framework.viewsets import ModelViewSet
from systemlog.models import SystemLog
from systemlog.serializers import SystemLogSerializer

class SystemLogViewSet(ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    
