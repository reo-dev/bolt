#-*- coding: cp949 -*-
from rest_framework.pagination import PageNumberPagination

class RequestPageNumberPagination(PageNumberPagination):
    page_size = 10

class AnswerPageNumberPagination(PageNumberPagination):
    page_size = 20