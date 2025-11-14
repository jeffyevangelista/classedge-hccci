from django.db import models

class SystemLog(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    entity_id = models.IntegerField()
    description = models.TextField()
    ip_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.action
        

    
    