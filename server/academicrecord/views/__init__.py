from .academic_year_views import AcademicYearViewSet
from .enrollment_views import EnrollmentViewSet
from .academic_term_category_views import AcademicTermCategoryViewSet
from .academic_term_views import AcademicTermViewSet
from .grading_period_category_views import GradingPeriodCategoryViewSet
from .grading_period_views import GradingPeriodViewSet

__all__ = [ 
            # Academic Year
            'AcademicYearViewSet',

            # Enrollement ViewSet
            'EnrollmentViewSet',

            # Academic Term Category ViewSet
            'AcademicTermCategoryViewSet',

            # Academic Term ViewSet
            'AcademicTermViewSet',

            # Grading Period Category ViewSet
            'GradingPeriodCategoryViewSet',
            
            # Grading Period ViewSet
            'GradingPeriodViewSet',
        ]
