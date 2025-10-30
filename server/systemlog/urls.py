from django.urls import path, include
from rest_framework.routers import DefaultRouter
from systemlog.views import SystemLogViewSet
router = DefaultRouter()

router.register(r'systemlog', SystemLogViewSet, basename='systemlog')

urlpatterns = [
    path('api/', include(router.urls)),
]