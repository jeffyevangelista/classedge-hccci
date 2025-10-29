from django.db import models
from django.conf import settings    

class Assessment(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey('teachingload.Subject', on_delete=models.PROTECT, related_name='assessments', null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assessments', null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    available_at = models.DateTimeField()
    due_at = models.DateTimeField()
    time_limit = models.IntegerField()
    max_attempts = models.IntegerField()
    late_penalty = models.DecimalField(max_digits=5, decimal_places=2)
    SCORING_POLICY_TYPE =[
        ('highest', 'Highest Score'),
        ('latest', 'Latest Take'),
        ('average', 'Average Score'),
        ('first', 'First Take'),
    ]
    scoring_policy = models.CharField(max_length=100, choices=SCORING_POLICY_TYPE)
    term = models.ForeignKey('academicrecord.Term', on_delete=models.PROTECT, related_name='assessments', null=True, blank=True)
    material = models.ManyToManyField('materials.Material', related_name='assessments', blank=True)
    submission_type = models.ForeignKey('SubmissionType', on_delete=models.PROTECT, related_name='assessments', null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    PASSING_SCORE_TYPE =[   
        ('number', 'Number'),
        ('percentage', 'Percentage'),
    ]
    passing_score_type = models.CharField(max_length=100, choices=PASSING_SCORE_TYPE)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2)
    is_classroom = models.BooleanField(default=False)
    is_shuffles = models.BooleanField(default=False)
    allowed_late = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    