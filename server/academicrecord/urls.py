from django.urls import path,include
from rest_framework.routers import DefaultRouter
from academicrecord.views import *

router = DefaultRouter()
router.register(r"academic-years", AcademicYearViewSet, basename='academic-year-view')
router.register(r"enrollments", EnrollmentViewSet, basename='enrollment-view')
router.register(r"academic-term-categories", AcademicTermCategoryViewSet, basename='academic-term-category-view')
router.register(r"academic-terms", AcademicTermViewSet, basename='academic-term-view')
router.register(r"grading-period-categories", GradingPeriodCategoryViewSet, basename='grading-period-category-view')
router.register(r"grading-periods", GradingPeriodViewSet, basename='grading-period-view')

urlpatterns = [
    path(
        "api/",
        include([
            path("", include(router.urls)),

        ])
    ),

]
