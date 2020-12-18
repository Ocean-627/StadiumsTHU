from django_filters import rest_framework as filters
from app.models import *


class UserFilter(filters.FilterSet):
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    nickName = filters.CharFilter(field_name='nickName', lookup_expr='icontains')
    userId = filters.CharFilter(field_name='userId', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')
    major = filters.CharFilter(field_name='major', lookup_expr='icontains')
    sort = filters.OrderingFilter(
        fields=('phone', 'name', 'nickName', 'userId', 'email', 'loginTime', 'inBlacklistTime'))

    class Meta:
        model = User
        fields = ['id', 'inBlacklist']


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
    stadium = filters.CharFilter(field_name='stadium', lookup_expr='icontains')
    court = filters.CharFilter(field_name='court', lookup_expr='icontains')
    sort = filters.OrderingFilter(fields=('createTime',))

    # TODO:更多筛选信息
    class Meta:
        model = ReserveEvent
        fields = ['id', 'stadium_id', 'user_id', 'duration_id', 'date', 'startTime', 'endTime', 'payment', 'cancel',
                  'checked', 'leave', 'has_comments']


class CommentFilter(filters.FilterSet):
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')
    sort = filters.OrderingFilter(fields=('createTime',))
    scoreLt = filters.NumberFilter(field_name='score', lookup_expr='lt')
    scoreGt = filters.NumberFilter(field_name='score', lookup_expr='gt')

    # TODO:更多筛选信息
    class Meta:
        model = Comment
        fields = ['id', 'court_id', 'reserve_id', 'stadium_id', 'user_id', 'score']


class CollectEventFilter(filters.FilterSet):
    class Meta:
        model = CollectEvent
        fields = ['id', 'stadium_id']


class ChangeDurationFilter(filters.FilterSet):
    # TODO:更多筛选条件
    class Meta:
        model = ChangeDuration
        fields = ['id', 'state']


class AddEventFilter(filters.FilterSet):
    # TODO:更多筛选条件
    class Meta:
        model = AddEvent
        fields = ['id', 'state']


class AddBlacklistFilter(filters.FilterSet):
    # TODO:更多筛选条件
    class Meta:
        model = AddBlacklist
        fields = ['id', 'state']


class DefaultFilter(filters.FilterSet):
    detail = filters.CharFilter(field_name='detail', lookup_expr='icontains')

    class Meta:
        model = Default
        fields = ['id', 'user_id', 'cancel', 'valid']


class NewsFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')
    sort = filters.OrderingFilter(fields=('createTime',))

    class Meta:
        model = News
        fields = ['id', 'checked']


class SessionFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('createTime', 'updateTime'))

    class Meta:
        model = Session
        fields = ['id', 'open', 'checked']


class MessageFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('createTime',))
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['id', 'session_id']
