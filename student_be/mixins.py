from django.db.models import Q
from django.core.cache import cache
from django.conf import settings

class SearchTermMixin:
    CACHE_TIMEOUT = getattr(settings, 'SEARCH_CACHE_TIMEOUT', 300)  # 5 minutes default

    def get_search_query(self, search_term, search_fields):
        """
        Tạo query tìm kiếm dựa trên search_term và các trường cần tìm
        """
        if not search_term:
            return Q()
        
        # Cache key for search query
        cache_key = f'search_query_{search_term}_{"_".join(search_fields)}'
        cached_query = cache.get(cache_key)
        
        if cached_query is not None:
            return cached_query
        
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_term})
            
        # Cache the query
        cache.set(cache_key, query, self.CACHE_TIMEOUT)
        return query

    def get_filtered_queryset(self, queryset, search_term, search_fields, **filters):
        """
        Lọc queryset dựa trên search_term và các filters
        """
        # Áp dụng tìm kiếm
        search_query = self.get_search_query(search_term, search_fields)
        queryset = queryset.filter(search_query)

        # Áp dụng các filters
        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset.distinct()  # Ensure unique results 