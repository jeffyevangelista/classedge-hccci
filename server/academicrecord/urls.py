from django.urls import path,include
from rest_framework.routers import DefaultRouter
from academicrecord.views import *

router = DefaultRouter()
router.register(r"academic-year", AcademicYearViewSet, basename='academic-year-view')
router.register(r"enrollment", EnrollmentViewSet, basename='enrollment-view')
router.register(r"semester", SemesterViewSet, basename='semester-view')
router.register(r"term", TermViewSet, basename='term-view')

urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),
        ])
    ),

]
