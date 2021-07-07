#-*- coding: cp949 -*-
from rest_framework.pagination import PageNumberPagination

class ClientPageNumberPagination(PageNumberPagination):
    page_size = 10

class PartnerPageNumberPagination(PageNumberPagination):
    page_size = 10
