from rest_framework.pagination import PageNumberPagination

class CityPageNumberPagination(PageNumberPagination):
    page_size = 15

class RegionPageNumberPagination(PageNumberPagination):
    page_size = 15