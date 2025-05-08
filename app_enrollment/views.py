from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer, EnrollmentDetailSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return EnrollmentDetailSerializer
        return EnrollmentSerializer
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            enrollments = Enrollment.objects.filter(student_id=student_id)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Student ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def by_class(self, request):
        class_id = request.query_params.get('class_id', None)
        if class_id:
            enrollments = Enrollment.objects.filter(class_id=class_id)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Class ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_val = request.query_params.get('status', None)
        if status_val:
            enrollments = Enrollment.objects.filter(status=status_val)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
