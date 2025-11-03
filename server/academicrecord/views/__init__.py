from .academic_year_views import AcademicYearViewSet
from .enrollment_views import EnrollmentViewSet
from .semester_views import SemesterViewSet
from .semester_category_views import SemesterCategoryViewSet
from .term_views import TermViewSet
from .term_category_views import TermCategoryViewSet

__all__ = [
            'AcademicYearViewSet',
            'EnrollmentViewSet',
            'SemesterViewSet',
            'TermViewSet',
            'SemesterCategoryViewSet',
            'TermCategoryViewSet',
        ]
