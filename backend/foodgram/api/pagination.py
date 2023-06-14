from rest_framework.pagination import PageNumberPagination

from foodgram import settings


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_query_param = 'page'
    page_size = settings.PAGE_SIZE
