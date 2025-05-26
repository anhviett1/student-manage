from rest_framework import serializers
from .models import Enrollment
from drf_spectacular.utils import extend_schema_serializer, extend_schema_field

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        
@extend_schema_serializer(component_name='EnrollmentCreateSerializer')
class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'subject', 'semester', 'status', 'enrollment_date']
        
@extend_schema_serializer(component_name='EnrollmentDetailSerializer')
class EnrollmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        depth = 1