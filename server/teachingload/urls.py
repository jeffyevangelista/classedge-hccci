from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename='subject-view')
router.register(r"schedules", ScheduleViewSet, basename='schedule-view')
router.register(r"schedule-types", ScheduleTypeViewSet, basename='schedule-type-view')
router.register(r"target-sdgs", SDGViewSet, basename='target-sdgs-view')
router.register(r"subject-offer", SubjectOfferingViewSet, basename='subject-offer-view')

urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),

        ])
    ),

]
