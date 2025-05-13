from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Semester
from .forms import SemesterForm

# Create your views here.

@login_required
def semester_list(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Base queryset
    semesters = Semester.objects.select_related('created_by').order_by('-created_at')

    # Apply filters
    if search_query:
        semesters = semesters.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if status_filter:
        semesters = semesters.filter(status=status_filter)

    # Pagination
    paginator = Paginator(semesters, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get status choices for filter
    status_choices = Semester.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    return render(request, 'app_semester_fe/semester_list.html', context)

@login_required
@permission_required('app_semester.can_manage_semester')
def semester_create(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.created_by = request.user
            semester.save()
            messages.success(request, 'Học kỳ đã được tạo thành công.')
            return redirect('semester_detail', pk=semester.pk)
    else:
        form = SemesterForm()

    context = {
        'form': form,
        'action': 'Thêm học kỳ',
    }
    return render(request, 'app_semester_fe/semester_form.html', context)

@login_required
def semester_detail(request, pk):
    semester = get_object_or_404(Semester.objects.select_related(
        'created_by'
    ).prefetch_related('subjects', 'enrollments'), pk=pk)
    return render(request, 'app_semester_fe/semester_detail.html', {'semester': semester})

@login_required
@permission_required('app_semester.can_manage_semester')
def semester_edit(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Học kỳ đã được cập nhật thành công.')
            return redirect('semester_detail', pk=semester.pk)
    else:
        form = SemesterForm(instance=semester)

    context = {
        'form': form,
        'action': 'Cập nhật học kỳ',
    }
    return render(request, 'app_semester_fe/semester_form.html', context)

@login_required
@permission_required('app_semester.can_manage_semester')
def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        semester.delete()
        messages.success(request, 'Học kỳ đã được xóa thành công.')
        return redirect('semester_list')
    return render(request, 'app_semester_fe/semester_confirm_delete.html', {'semester': semester})
