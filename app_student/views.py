from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer, StudentDetailSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_deleted=False)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return StudentDetailSerializer
        return StudentSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_students = Student.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)
