from django.db import models    
import uuid
import os
from django.conf import settings

def get_upload_path_profile(instance, filename):
    filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    return os.path.join('profile', filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    STATUS_TYPE = [
        ('Regular', 'Regular'),
        ('Irregular', 'Irregular'),
    ]
    student_status = models.CharField(max_length=15, choices=STATUS_TYPE, null=True, blank=True)

    #Personal Information
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to= get_upload_path_profile, null=True, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)

    #Contact Information
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    #Academic Information
    id_number = models.CharField(max_length=255, null=True, blank=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)
    YEAR_LEVEL_CHOICES = [
        ('1st Year College', '1st Year College'),
        ('2nd Year College', '2nd Year College'),
        ('3rd Year College', '3rd Year College'),
        ('4th Year College', '4th Year College'),
    ]
    #for student
    grade_year_level = models.CharField(max_length=255, choices=YEAR_LEVEL_CHOICES, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    
    #for teacher and staff
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    is_coil_user = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"