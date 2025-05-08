from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer, TeacherDetailSerializer

# Create your views here.

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return TeacherDetailSerializer
        return TeacherSerializer
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject = request.query_params.get('subject', None)
        if subject:
            teachers = Teacher.objects.filter(subject=subject)
            serializer = self.get_serializer(teachers, many=True)
            return Response(serializer.data)
        return Response({"error": "Subject parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
