from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Class
from .serializers import ClassSerializer, ClassCreateSerializer, ClassDetailSerializer
from .forms import ClassForm
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Classes']),
    retrieve=extend_schema(tags=['Classes']),
    create=extend_schema(tags=['Classes']),
    update=extend_schema(tags=['Classes']),
    partial_update=extend_schema(tags=['Classes']),
    destroy=extend_schema(tags=['Classes']),
    by_instructor=extend_schema(tags=['Classes']),
)
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

@login_required
def class_list(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Base queryset
    classes = Class.objects.select_related('created_by').order_by('-created_at')

    # Apply filters
    if search_query:
        classes = classes.filter(
            Q(class_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(faculty__icontains=search_query)
        )
    if status_filter:
        classes = classes.filter(status=status_filter)

    # Pagination
    paginator = Paginator(classes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get status choices for filter
    status_choices = Class.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    return render(request, 'app_class_fe/class_list.html', context)

@login_required
@permission_required('app_class.can_manage_class')
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.created_by = request.user
            class_obj.save()
            messages.success(request, 'Lớp học đã được tạo thành công.')
            return redirect('class_detail', pk=class_obj.pk)
    else:
        form = ClassForm()

    context = {
        'form': form,
        'action': 'Thêm lớp học',
    }
    return render(request, 'app_class_fe/class_form.html', context)

@login_required
def class_detail(request, pk):
    class_obj = get_object_or_404(Class.objects.select_related(
        'created_by'
    ).prefetch_related('students'), pk=pk)
    return render(request, 'app_class_fe/class_detail.html', {'class': class_obj})

@login_required
@permission_required('app_class.can_manage_class')
def class_edit(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lớp học đã được cập nhật thành công.')
            return redirect('class_detail', pk=class_obj.pk)
    else:
        form = ClassForm(instance=class_obj)

    context = {
        'form': form,
        'action': 'Cập nhật lớp học',
    }
    return render(request, 'app_class_fe/class_form.html', context)

@login_required
@permission_required('app_class.can_manage_class')
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Lớp học đã được xóa thành công.')
        return redirect('class_list')
    return render(request, 'app_class_fe/class_confirm_delete.html', {'class': class_obj})
