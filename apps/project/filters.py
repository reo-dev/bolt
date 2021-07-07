#-*- coding: cp949 -*-
import django_filters
from rest_framework import filters
from django.db.models import (
    Case,
    Count,
    When,
)

from apps.project.models import *

class RequestFilter(filters.BaseFilterBackend): # �Ķ���� ���� �� ������ or�� �������� ����

        def filter_queryset(self, request, queryset, view):  ## ���� �θ� �� �ڵ�
          data=request.GET
          data_dict = data.dict() # dictionary ȭ

          if  'product__id' in data_dict:
                data = data['product__id'].split(',')
                return queryset.filter(product__in=data).distinct('id')

          elif 'client__id' in data_dict:
                   data = data['client__id'].split(',')
                   return queryset.filter(client__in=data).distinct('id')

          return queryset.filter()

class ProjectFilter(filters.BaseFilterBackend): # �Ķ���� ���� �� ������ or�� �������� ����

        def filter_queryset(self, request, queryset, view):  ## ���� �θ� �� �ڵ�
          data=request.GET
          data_dict = data.dict() # dictionary ȭ

          if 'client__id' in data_dict:
                   data = data['client__id'].split(',')
                   return queryset.filter(client__in=data).distinct('id')

          return queryset.filter()