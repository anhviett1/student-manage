from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name")
    semester_name = serializers.ReadOnlyField(source="semester.name")

    class Meta:
        model = Subject
        fields = [f.name for f in Subject._meta.fields] + ["department_name", "semester_name"]
        read_only_fields = ["subject_id", "created_at", "updated_at"]
