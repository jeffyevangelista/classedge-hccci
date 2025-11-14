from .teaching_load_views import SubjectViewSet
from .teaching_load_schedule_views import ScheduleViewSet
from .schedule_type_views import ScheduleTypeViewSet
from .target_sdgs_views import SDGViewSet
from .subject_offering_views import SubjectOfferingViewSet

__all__ = [
            'SubjectViewSet',
            'ScheduleViewSet',
            'ScheduleTypeViewSet',
            'SDGViewSet',
            'SubjectOfferingViewSet',
        ]
