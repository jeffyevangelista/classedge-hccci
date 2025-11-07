from django.db import models

class Schedule(models.Model):
    subject_id = models.ForeignKey('Subject', on_delete=models.PROTECT,null=True,blank=True)
    schedule_type_id = models.ForeignKey('ScheduleType', on_delete=models.PROTECT,null=True,blank=True)
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    days = models.CharField(max_length=255, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    academic_term_id = models.ForeignKey('academicrecord.AcademicTerm', related_name='teaching_load_schedules', on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.subject_id.name} - {self.days} - {self.start_time} - {self.end_time}"