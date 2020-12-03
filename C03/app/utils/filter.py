from django_filters import rest_framework as filters
from app.models import *


class UserFilter(filters.FilterSet):
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    nickName = filters.CharFilter(field_name='nickName', lookup_expr='icontains')
    userId = filters.CharFilter(field_name='userId', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    sort = filters.OrderingFilter(fields=('phone', 'name', 'nickName', 'userId', 'email'))

    class Meta:
        model = User
        fields = ['id', 'auth']


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
        fields = ['id', 'stadium_id', 'openState', 'floor', 'location']


class CourtTypeFilter(filters.FilterSet):
    class Meta:
        model = CourtType
        fields = ['stadium_id']


class DurationFilter(filters.FilterSet):
    # TODO:更多筛选信息
    class Meta:
        model = Duration
        fields = ['id', 'stadium_id', 'court_id', 'openState', 'accessible', 'startTime', 'date']


class ReserveEventFilter(filters.FilterSet):
    # TODO:更多筛选信息
    class Meta:
        model = ReserveEvent
        fields = ['id', 'user_id', 'stadium_id', 'court_id', 'duration_id', 'startTime', 'endTime']


class CommentFilter(filters.FilterSet):
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    # TODO:更多筛选信息
    class Meta:
        model = Comment
        fields = ['id', 'court_id']


class CollectEventFilter(filters.FilterSet):
    class Meta:
        model = CollectEvent
        fields = ['id', 'stadium_id']


class ChangeDurationFilter(filters.FilterSet):
    class Meta:
        model = ChangeDuration
        fields = ['id']
