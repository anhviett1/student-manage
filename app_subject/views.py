from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from student_be.mixins import SearchTermMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Subject
from .serializers import SubjectSerializer, SubjectCreateSerializer, SubjectDetailSerializer
from .forms import SubjectForm

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

class SubjectSearchMixin(SearchTermMixin):
    search_fields = ['subject_id', 'name', 'description', 'faculty']

@login_required
def subject_list(request):
    search_mixin = SubjectSearchMixin()
    search_term = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    faculty_filter = request.GET.get('faculty', '')

    # Base queryset
    subjects = Subject.objects.select_related('teacher', 'created_by').order_by('-created_at')

    # Apply search and filters
    subjects = search_mixin.get_filtered_queryset(
        subjects,
        search_term,
        search_mixin.search_fields,
        status=status_filter if status_filter else None,
        faculty=faculty_filter if faculty_filter else None
    )

    # Pagination
    paginator = Paginator(subjects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'status_filter': status_filter,
        'faculty_filter': faculty_filter,
        'status_choices': Subject.STATUS_CHOICES,
        'faculty_choices': Subject.FACULTY_CHOICES,
    }
    return render(request, 'app_subject_fe/subject_list.html', context)
