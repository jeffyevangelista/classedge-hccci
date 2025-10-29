from django.db import models
import os
import uuid



def get_upload_path_material_attachment(instance, filename):
    filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    return os.path.join('material_attachments', filename)

class MaterialAttachment(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path_material_attachment)
    url = models.URLField()
    type = models.CharField(max_length=255)