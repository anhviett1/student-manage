from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Subject
from .serializers import SubjectSerializer, SubjectCreateSerializer, SubjectDetailSerializer

# Create your views here.

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubjectCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return SubjectDetailSerializer
        return SubjectSerializer
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        teacher_id = request.query_params.get('teacher_id', None)
        if teacher_id:
            subjects = Subject.objects.filter(teacher_id=teacher_id)
            serializer = self.get_serializer(subjects, many=True)
            return Response(serializer.data)
        return Response({"error": "Teacher ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
