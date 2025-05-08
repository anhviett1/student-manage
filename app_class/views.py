from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Class
from .serializers import ClassSerializer, ClassCreateSerializer, ClassDetailSerializer

# Create your views here.

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ClassCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ClassDetailSerializer
        return ClassSerializer
    
    @action(detail=False, methods=['get'])
    def by_instructor(self, request):
        instructor = request.query_params.get('instructor', None)
        if instructor:
            classes = Class.objects.filter(instructor=instructor)
            serializer = self.get_serializer(classes, many=True)
            return Response(serializer.data)
        return Response({"error": "Instructor parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
