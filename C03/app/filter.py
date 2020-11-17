from django_filters import rest_framework as filters
from app.models import *


class BookFilter(filters.FilterSet):
    class Meta:
        min_read = filters.NumberFilter(field_name="bread", lookup_expr='gte')
        max_read = filters.NumberFilter(field_name="bread", lookup_expr='lte')
        model = Bookinfo  # 模型名
        fields = {
            'btitle': ['icontains'],
            'bcomment': ['gte', 'lte'],
        }
