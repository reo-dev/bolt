#-*- coding: cp949 -*-
import django_filters
from rest_framework import filters
from django.db.models import (
    Case,
    Count,
    When,
)

from apps.account.models import *
from functools import reduce
import operator
from rest_framework.compat import coreapi, coreschema, distinct
from konlpy.tag import Kkma

class PartnerFilter(filters.BaseFilterBackend): # 파라미터 여러 개 보내도 or로 가져오는 필터

        def filter_queryset(self, request, queryset, view):  ## 필터 부를 때 자동
          data=request.GET
          data_dict = data.dict() # dictionary 화
          if  'category_exclude' in data_dict:
                data2 = data['category_exclude'].split(',')
                queryset = queryset.exclude(category_middle__in=data2)

          if  'region' in data_dict:
                data2 = data['region'].split(',')
                queryset = queryset.filter(region__in=data2)

          if 'city' in data_dict:
                data2 = data['city'].split(',')
                queryset = queryset.filter(city__in=data2)

          if 'category_middle__id' in data_dict:
                data2 = data['category_middle__id'].split(',')
                queryset = queryset.filter(category_middle__in=data2)

          if 'history_set__id' in data_dict:
                data2 = data['history_set__id'].split(',')
                queryset = queryset.filter(history_set__in=data2)

          if 'history' in data_dict:
                data2 = data['history']
                queryset = queryset.filter(history__contains=data2)

          return queryset



class CustomSearchFilter(filters.SearchFilter):
      def filter_queryset(self, request, queryset, view):
            search_fields = self.get_search_fields(view, request)
            search_terms = self.get_search_terms(request)
            if not search_fields or not search_terms:
                  return queryset

            orm_lookups = [self.construct_search(str(search_field)) for search_field in search_fields]

            base = queryset
            conditions = []
            partner_id = []
            kkma = Kkma()

            for search_term in search_terms:
                  x = kkma.morphs(search_term)
                  for i in x:
                        queries = [models.Q(**{orm_lookup: i}) for orm_lookup in orm_lookups]
                        conditions.append(reduce(operator.or_, queries))
                        portfolio = Portfolio.objects.filter(name__icontains=i)
                        for j in portfolio:
                              if j.partner.id not in partner_id:
                                    partner_id.append(j.partner.id)
            partner = Partner.objects.filter(id__in=partner_id).order_by('id').distinct()
            partner2= Partner.objects.filter(name='서울기전').order_by('id').distinct()
            queryset = queryset.filter(reduce(operator.and_, conditions)).order_by('id').distinct()
            queryset = queryset.union(partner)
            if self.must_call_distinct(queryset, search_fields):
                  queryset = distinct(queryset, base)
            return queryset

    