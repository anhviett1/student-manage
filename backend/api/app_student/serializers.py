from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source="user.get_full_name")
    department_name = serializers.ReadOnlyField(source="department.name")
    class_assigned_names = serializers.SerializerMethodField()
    subject_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="subjects")
    score_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="scores")

    def get_class_assigned_names(self, obj):
        return [class_obj.name for class_obj in obj.class_assigned.all()]

    class Meta:
        model = Student
        fields = [f.name for f in Student._meta.fields] + [
            "user_full_name",
            "department_name",
            "class_assigned_names",
            "full_name",
            "subject_ids",
            "score_ids",
        ]
        read_only_fields = ["student_id", "created_at", "updated_at", "deleted_at", "gpa"]
