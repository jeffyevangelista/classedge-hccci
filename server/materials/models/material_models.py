from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey('teachingload.Subject', on_delete=models.CASCADE)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    term = models.ForeignKey('academicrecord.Term', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        