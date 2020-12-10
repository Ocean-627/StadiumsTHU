from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'


class UserPagination(BasePagination):
    page_size = 10
    max_page_size = 30


class SessionPagination(BasePagination):
    page_size = 10
    max_page_size = 30

