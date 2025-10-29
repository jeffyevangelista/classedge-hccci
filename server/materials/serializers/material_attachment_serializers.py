from rest_framework import serializers
from materials.models import MaterialAttachment

class MaterialAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialAttachment
        fields = '__all__'
    