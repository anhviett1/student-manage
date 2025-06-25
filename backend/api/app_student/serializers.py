from rest_framework import serializers
from .models import Student



class StudentSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "name",
            "email",
            "phone",
            "department",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["student_id", "created_at", "updated_at"]
    
