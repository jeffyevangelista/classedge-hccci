from django.urls import path,include
from rest_framework.routers import DefaultRouter
from materials.views import MaterialViewSet, MaterialAttachmentViewSet

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'material-attachments', MaterialAttachmentViewSet, basename='material-attachment')


urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),
        ])
    ),
    

]
