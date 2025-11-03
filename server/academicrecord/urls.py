from django.urls import path,include
from rest_framework.routers import DefaultRouter
from academicrecord.views import *

router = DefaultRouter()
router.register(r"academic-years", AcademicYearViewSet, basename='academic-year-view')
router.register(r"semester-categories", SemesterCategoryViewSet, basename='semester-category-view')
router.register(r"enrollments", EnrollmentViewSet, basename='enrollment-view')
router.register(r"semesters", SemesterViewSet, basename='semester-view')
router.register(r"terms", TermViewSet, basename='term-view')
router.register(r"term-categories", TermCategoryViewSet, basename='term-category-view')

urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),

            path("academic-years/all/", GenericAcademicYearViewSet.as_view(), name="academic-year-generic-view"),
        ])
    ),

]
