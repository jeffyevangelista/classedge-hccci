from rest_framework import serializers
from academicrecord.models import Term

class TermSerializer(serializers.ModelSerializer):
    semester = serializers.CharField(source='semester_id.name')
    term_category = serializers.CharField(source='term_category_id.name')

    class Meta:
        model = Term
        fields = '__all__'
