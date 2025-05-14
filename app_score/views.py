from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.core.cache import cache
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from student_be.mixins import SearchTermMixin
from .models import Score
from .serializers import ScoreSerializer, ScoreCreateSerializer, ScoreDetailSerializer
from .forms import ScoreForm
from app_subject.models import Subject
from app_semester.models import Semester
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Scores']),
    retrieve=extend_schema(tags=['Scores']),
    create=extend_schema(tags=['Scores']),
    update=extend_schema(tags=['Scores']),
    partial_update=extend_schema(tags=['Scores']),
    destroy=extend_schema(tags=['Scores']),
    by_student=extend_schema(tags=['Scores']),
    by_subject=extend_schema(tags=['Scores']),
)
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ).prefetch_related(
        Prefetch('student__scores', queryset=Score.objects.select_related('subject', 'semester'))
    )
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
        if not student_id:
            return Response({"error": "Student ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        cache_key = f'student_scores_{student_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        scores = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(scores, many=True)
        
        cache.set(cache_key, serializer.data, settings.CACHE_TIMEOUT)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject_id = request.query_params.get('subject_id', None)
        if not subject_id:
            return Response({"error": "Subject ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        cache_key = f'subject_scores_{subject_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        scores = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(scores, many=True)
        
        cache.set(cache_key, serializer.data, settings.CACHE_TIMEOUT)
        return Response(serializer.data)

class ScoreSearchMixin(SearchTermMixin):
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name',
                    'subject__name', 'semester__name']

@login_required
def score_list(request):
    search_mixin = ScoreSearchMixin()
    search_term = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    semester_filter = request.GET.get('semester', '')

    # Cache key for filtered queryset
    cache_key = f'score_list_{search_term}_{subject_filter}_{semester_filter}'
    cached_page = cache.get(cache_key)
    
    if cached_page is not None:
        return render(request, 'app_score_fe/score_list.html', cached_page)

    # Base queryset with optimized prefetching
    scores = Score.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ).prefetch_related(
        Prefetch('student__scores', queryset=Score.objects.select_related('subject', 'semester'))
    ).order_by('-created_at')

    # Apply search and filters
    scores = search_mixin.get_filtered_queryset(
        scores,
        search_term,
        search_mixin.search_fields,
        subject_id=subject_filter if subject_filter else None,
        semester_id=semester_filter if semester_filter else None
    )

    # Pagination
    paginator = Paginator(scores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Cache subjects and semesters
    subjects = cache.get('active_subjects')
    if subjects is None:
        subjects = Subject.objects.filter(is_active=True)
        cache.set('active_subjects', subjects, settings.CACHE_TIMEOUT)
        
    semesters = cache.get('active_semesters')
    if semesters is None:
        semesters = Semester.objects.filter(is_active=True)
        cache.set('active_semesters', semesters, settings.CACHE_TIMEOUT)

    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'subject_filter': subject_filter,
        'semester_filter': semester_filter,
        'subjects': subjects,
        'semesters': semesters,
    }
    
    # Cache the context
    cache.set(cache_key, context, settings.CACHE_TIMEOUT)
    return render(request, 'app_score_fe/score_list.html', context)

@login_required
@permission_required('app_score.can_manage_score')
def score_create(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.created_by = request.user
            score.save()
            
            # Clear relevant caches
            cache.delete_pattern('score_list_*')
            cache.delete_pattern('student_scores_*')
            cache.delete_pattern('subject_scores_*')
            
            messages.success(request, 'Điểm đã được thêm thành công.')
            return redirect('score_detail', pk=score.pk)
    else:
        form = ScoreForm()

    context = {
        'form': form,
        'action': 'Thêm điểm',
    }
    return render(request, 'app_score_fe/score_form.html', context)

@login_required
def score_detail(request, pk):
    cache_key = f'score_detail_{pk}'
    cached_score = cache.get(cache_key)
    
    if cached_score is not None:
        return render(request, 'app_score_fe/score_detail.html', {'score': cached_score})
        
    score = get_object_or_404(Score.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ).prefetch_related(
        Prefetch('student__scores', queryset=Score.objects.select_related('subject', 'semester'))
    ), pk=pk)
    
    cache.set(cache_key, score, settings.CACHE_TIMEOUT)
    return render(request, 'app_score_fe/score_detail.html', {'score': score})

@login_required
@permission_required('app_score.can_manage_score')
def score_edit(request, pk):
    score = get_object_or_404(Score, pk=pk)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            
            # Clear relevant caches
            cache.delete_pattern('score_list_*')
            cache.delete_pattern('student_scores_*')
            cache.delete_pattern('subject_scores_*')
            cache.delete(f'score_detail_{pk}')
            
            messages.success(request, 'Điểm đã được cập nhật thành công.')
            return redirect('score_detail', pk=score.pk)
    else:
        form = ScoreForm(instance=score)

    context = {
        'form': form,
        'action': 'Cập nhật điểm',
    }
    return render(request, 'app_score_fe/score_form.html', context)

@login_required
@permission_required('app_score.can_manage_score')
def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    if request.method == 'POST':
        score.delete()
        
        # Clear relevant caches
        cache.delete_pattern('score_list_*')
        cache.delete_pattern('student_scores_*')
        cache.delete_pattern('subject_scores_*')
        cache.delete(f'score_detail_{pk}')
        
        messages.success(request, 'Điểm đã được xóa thành công.')
        return redirect('score_list')
    return render(request, 'app_score_fe/score_confirm_delete.html', {'score': score})
