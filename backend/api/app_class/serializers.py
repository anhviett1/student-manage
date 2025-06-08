from rest_framework import serializers
from .models import Class
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
class ClassSerializer(serializers.ModelSerializer):
    """Serializer cho model Class"""
    created_by = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )
    updated_by = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Class
        fields = [
            'class_id', 'name', 'subject', 'semester', 'teacher', 'room',
            'schedule', 'max_students', 'current_students', 'status',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Kiểm tra logic hợp lệ của các trường"""
        max_students = data.get('max_students')
        current_students = data.get('current_students')

        if max_students is not None and current_students is not None:
            if current_students > max_students:
                raise serializers.ValidationError(_('Số học sinh hiện tại không thể lớn hơn số học sinh tối đa.'))

        return data      
