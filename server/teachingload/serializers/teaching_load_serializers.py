from rest_framework import serializers
from teachingload.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    sdgs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='target_sdgs_id',
    )
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            url = obj.photo.url
            return request.build_absolute_uri(url) if request else url
        return None
