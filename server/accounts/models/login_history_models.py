from django.db import models
from django.utils.timezone import now
from django.conf import settings

class LoginHistory(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"