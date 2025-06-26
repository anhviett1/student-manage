from rest_framework import serializers
from .models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
        read_only_fields = ["semester_id", "created_at", "updated_at"]