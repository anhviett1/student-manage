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
from student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Score
from .serializers import ScoreSerializer, ScoreCreateSerializer, ScoreDetailSerializer
from .forms import ScoreForm
from app_subject.models import Subject
from app_semester.models import Semester
from app_home.permissions import IsAdmin, IsTeacher, CanManageScores, CanViewOwnScores
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Scores']),
    retrieve=extend_schema(tags=['Scores']),
    create=extend_schema(tags=['Scores']),
    update=extend_schema(tags=['Scores']),
    partial_update=extend_schema(tags=['Scores']),
    destroy=extend_schema(tags=['Scores']),
    my_scores=extend_schema(tags=['Scores']),
)
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.filter(is_deleted=False)
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated, CanManageScores]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ScoreDetailSerializer
        return ScoreSerializer
    
    def get_permissions(self):
        if self.action == 'my_scores':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def my_scores(self, request):
        if request.user.role == 'student':
            scores = Score.objects.filter(
                student__user=request.user,
                is_deleted=False
            )
        elif request.user.role == 'teacher':
            scores = Score.objects.filter(
                subject__teacher__user=request.user,
                is_deleted=False
            )
        else:
            scores = Score.objects.filter(is_deleted=False)
            
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

class ScoreListView(BaseListView):
    model = Score
    template_name = 'app_score_fe/score_list.html'
    context_object_name = 'scores'
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        subject_filter = self.request.GET.get('subject', '')
        semester_filter = self.request.GET.get('semester', '')
        status_filter = self.request.GET.get('status', '')
        
        if subject_filter:
            queryset = queryset.filter(subject=subject_filter)
        if semester_filter:
            queryset = queryset.filter(semester=semester_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related(
            'student', 'subject', 'semester', 'created_by'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'subject_filter': self.request.GET.get('subject', ''),
            'semester_filter': self.request.GET.get('semester', ''),
            'status_filter': self.request.GET.get('status', ''),
            'status_choices': Score.STATUS_CHOICES,
        })
        return context

class ScoreDetailView(BaseDetailView):
    model = Score
    template_name = 'app_score_fe/score_detail.html'
    context_object_name = 'score'
    
    def get_queryset(self):
        return Score.objects.select_related(
            'student', 'subject', 'semester', 'created_by'
        )

class ScoreCreateView(BaseCreateView):
    model = Score
    form_class = ScoreForm
    template_name = 'app_score_fe/score_form.html'
    success_url = 'scores:score_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm điểm số'
        return context

class ScoreUpdateView(BaseUpdateView):
    model = Score
    form_class = ScoreForm
    template_name = 'app_score_fe/score_form.html'
    success_url = 'scores:score_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật điểm số'
        return context

class ScoreDeleteView(BaseDeleteView):
    model = Score
    template_name = 'app_score_fe/score_confirm_delete.html'
    success_url = 'scores:score_list'
    
    def delete(self, request, *args, **kwargs):
        score = self.get_object()
        score.is_deleted = True
        score.save()
        messages.success(request, 'Điểm số đã được xóa thành công.')
        return redirect(self.success_url)

class ScoreSearchMixin(SearchTermMixin):
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name',
                    'subject__name', 'semester__name']

@login_required
def score_list(request):
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    semester_filter = request.GET.get('semester', '')
    status_filter = request.GET.get('status', '')

    # Base queryset
    scores = Score.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ).order_by('-created_at')

    # Apply filters
    if search_query:
        scores = scores.filter(
            Q(student__student_id__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query)
        )
    if subject_filter:
        scores = scores.filter(subject_id=subject_filter)
    if semester_filter:
        scores = scores.filter(semester_id=semester_filter)
    if status_filter:
        scores = scores.filter(status=status_filter)

    # Pagination
    paginator = Paginator(scores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    subjects = Subject.objects.filter(is_active=True)
    semesters = Semester.objects.filter(is_active=True)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'semester_filter': semester_filter,
        'status_filter': status_filter,
        'subjects': subjects,
        'semesters': semesters,
        'status_choices': Score.STATUS_CHOICES,
    }
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
    score = get_object_or_404(Score.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ), pk=pk)
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
