
from .profile_views import ProfileViewSet, oauth2_login, oauth2_callback, test_session  
from .login_history_views import LoginHistoryViewSet
from .role_views import RoleViewSet
from .department_views import DepartmentViewSet
from .display_image_views import DisplayImageViewSet
from .course_views import CourseViewSet
from .badge_views import BadgeViewSet
from .certificate_views import CertificateViewSet


__all__ = [
            # Profile 
            'ProfileViewSet',
            'oauth2_login',
            'oauth2_callback',
            'test_session',
            
            # Login History
            'LoginHistoryViewSet',
            
            # Role 
            'RoleViewSet',
            
            # Department
            'DepartmentViewSet',
            
            # Display Image
            'DisplayImageViewSet',
            
            # Course
            'CourseViewSet',
            
            # Badge
            'BadgeViewSet',
            
            # Certificate
            'CertificateViewSet',
        ]










