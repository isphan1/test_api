from rest_framework import pagination


class apiPageSize(pagination.PageNumberPagination):

    page_size = 5