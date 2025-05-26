from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .mixins import StaffRequiredMixin, SuperuserRequiredMixin, SearchTermMixin

class BaseListView(LoginRequiredMixin, StaffRequiredMixin, ListView, SearchTermMixin):
    template_name = None
    context_object_name = 'object_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.get_search_query(self.request)
        if search_query:
            queryset = queryset.filter(search_query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class BaseDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    template_name = None
    context_object_name = 'object'

class BaseCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    template_name = None
    success_url = None
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'{self.model.__name__} đã được tạo thành công.')
        return super().form_valid(form)

class BaseUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    template_name = None
    success_url = None
    
    def form_valid(self, form):
        messages.success(self.request, f'{self.model.__name__} đã được cập nhật thành công.')
        return super().form_valid(form)

class BaseDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    template_name = None
    success_url = None
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'{self.model.__name__} đã được xóa thành công.')
        return super().delete(request, *args, **kwargs) 