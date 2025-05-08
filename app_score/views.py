from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Score
from .serializers import ScoreSerializer, ScoreCreateSerializer, ScoreDetailSerializer

# Create your views here.

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ScoreDetailSerializer
        return ScoreSerializer
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            scores = Score.objects.filter(student_id=student_id)
            serializer = self.get_serializer(scores, many=True)
            return Response(serializer.data)
        return Response({"error": "Student ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject_id = request.query_params.get('subject_id', None)
        if subject_id:
            scores = Score.objects.filter(subject_id=subject_id)
            serializer = self.get_serializer(scores, many=True)
            return Response(serializer.data)
        return Response({"error": "Subject ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
