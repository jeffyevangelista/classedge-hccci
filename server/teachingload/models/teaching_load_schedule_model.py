from django.db import models

class Schedule(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    schedule_type = models.ForeignKey('ScheduleType', on_delete=models.CASCADE)
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
    semester = models.ForeignKey('academicrecord.Semester', related_name='teaching_load_schedules', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.subject.name} - {self.days} - {self.start_time} - {self.end_time}"