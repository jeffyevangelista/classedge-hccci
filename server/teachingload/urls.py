from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"subject", SubjectViewSet, basename='subject-view')
router.register(r"schedule", ScheduleViewSet, basename='schedule-view')
router.register(r"schedule-type", ScheduleTypeViewSet, basename='schedule-type-view')
router.register(r"target-sdgs", SDGViewSet, basename='target-sdgs-view')
router.register(r"subject-offering", SubjectOfferingViewSet, basename='subject-offering-view')

urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),

        ])
    ),

]
