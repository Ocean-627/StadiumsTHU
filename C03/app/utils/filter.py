from django_filters import rest_framework as filters
from app.models import *


class StadiumFilter(filters.FilterSet):
    # TODO:更多筛选信息
    infoKey = filters.CharFilter(field_name='information', lookup_expr='icontains')
    nameKey = filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Stadium
        fields = ['openState', 'foreDays']


class CourtFilter(filters.FilterSet):
    # TODO:更多筛选信息
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')
    priceGt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    priceLt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Court
        fields = ['stadium_id', 'openState', 'floor', 'location']


class DurationFilter(filters.FilterSet):
    # TODO:更多筛选信息
    class Meta:
        model = Duration
        fields = ['stadium_id', 'court_id', 'openState', 'accessible']
