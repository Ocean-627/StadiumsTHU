from django_filters import rest_framework as filters
from app.models import *


class StadiumFilter(filters.FilterSet):
    # TODO:更多筛选信息
    info = filters.CharFilter(field_name='information', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    foreGt = filters.NumberFilter(field_name='foreDays', lookup_expr='gt')

    class Meta:
        model = Stadium
        fields = ['id', 'openState', 'foreDays']


class CourtFilter(filters.FilterSet):
    # TODO:更多筛选信息
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')
    priceGt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    priceLt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    sort = filters.OrderingFilter(fields=('price',))

    class Meta:
        model = Court
        fields = ['stadium_id', 'openState', 'floor', 'location']


class DurationFilter(filters.FilterSet):
    # TODO:更多筛选信息
    class Meta:
        model = Duration
        fields = ['stadium_id', 'court_id', 'openState', 'accessible', 'startTime']


class ReserveEventFilter(filters.FilterSet):
    # TODO:更多筛选信息
    class Meta:
        model = ReserveEvent
        fields = ['stadium_id', 'court_id', 'duration_id', 'startTime', 'endTime']


class CommentFilter(filters.FilterSet):
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    # TODO:更多筛选信息
    class Meta:
        model = Comment
        fields = ['court_id']
