from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 30
