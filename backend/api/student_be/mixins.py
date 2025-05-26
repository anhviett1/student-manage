from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

def staff_required(view_func):
    decorated_view = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view

def superuser_required(view_func):
    decorated_view = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view

class SearchTermMixin:
    CACHE_TIMEOUT = getattr(settings, 'SEARCH_CACHE_TIMEOUT', 300)  # 5 minutes default
    search_fields = []

    def get_search_query(self, request):
        search_query = request.GET.get('search', '')
        if search_query and self.search_fields:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search_query})
            return query
        return None

    def get_filtered_queryset(self, queryset, search_term, search_fields, **filters):
        """
        Lọc queryset dựa trên search_term và các filters
        """
        # Áp dụng tìm kiếm
        search_query = self.get_search_query(self.request)
        queryset = queryset.filter(search_query)

        # Áp dụng các filters
        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset.distinct()  # Ensure unique results 