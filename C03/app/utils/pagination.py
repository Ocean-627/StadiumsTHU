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


class CommentPagination(BasePagination):
    page_size = 10
    max_page_size = 30


class ReserveHistoryPagination(BasePagination):
    page_size = 15
    max_page_size = 30


class DefaultPagination(BasePagination):
    page_size = 15
    max_page_size = 30


class NewsPagination(BasePagination):
    page_size = 20
    max_page_size = 30


class MyPagination(object):

    def __init__(self, max_page_size=30):
        self.max_page_size = max_page_size

    def paginate(self, queryset, page, size):
        left = (page - 1) * size
        right = page * size
        if left >= len(queryset):
            res = []
        else:
            res = queryset[left:right]
        return {
            'count': len(queryset),
            'results': res
        }
