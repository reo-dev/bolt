#-- coding: cp949 --

from rest_framework import (
    viewsets,
    status,
    mixins,
)
from django.conf import settings
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.log.models import *
from apps.log.cron import *
from apps.account.setting_bulk import *
from apps.utils import *
from .serializers import *
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from elasticsearch import Elasticsearch  
import requests





import pprint
import requests
from lxml import etree
from argparse import ArgumentParser
import sys




class ClickLogViewSet (viewsets.ModelViewSet):
    serializer_class = ClickLogSerializer
    queryset = clickLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))
        if ip !='0.0.0.0':
            serializer.save(ip=ip)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PageAccessLogViewSet (viewsets.ModelViewSet):
    serializer_class = PageAccessLogSerializer
    queryset = PageAccessLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))
        if ip !='0.0.0.0':
            serializer.save(ip=ip)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AccessLogViewSet (viewsets.ModelViewSet):
    serializer_class = AccessLogSerializer
    queryset = AccessLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']

    def create(self, request, *args, **kwargs):
        # postDayLog()
        # postUserLog()
        # imgUpload.save()
        # imgUpload.remove()
        # imgUpload.googleUpload()
        # imgUpload.fileupload()
        # elastic.send()
        qweqw='bolt'
        params = {'output':'toolbar','q':qweqw}
        a = requests.get('https://suggestqueries.google.com/complete/search',params=params)
        print(a.url)
        root = etree.XML(a.text)
        sugs = root.xpath('//suggestion')
        sugstrs = [s.get('data') for s in sugs]

    
        y = ' '.join(sugstrs)
        print(y)
        es = Elasticsearch("http://localhost:9200", timeout=100, max_retries=10, retry_on_timeout=True)
        partner = es.search(
            index='partner-2',
            body={
                'size':10000,
                "query": {
                    "multi_match": {
                        "query": y,
                        "fields": [
                            "name.english_field",
                            "info_company.english_field",
                            "info_company.korean_field"
                            "name.korean_field"
                        ]

                    }
                }
            })

        print(partner)
        # portfolio = es.search(
        #     index='port-5',
        #     body={
        #         'size':10000,
        #         "query": {
        #             "multi_match": {
        #                 "query": y,
        #                 "fields": [
        #                     "name"
        #                 ]
        #             }
        #         }
        #     })
        # print(portfolio)
        
        data_list = []
        for data in partner['hits']['hits']:
            data_list.append(data.get('_source'))
        print('hello3',data_list[0],len(data_list))

        # data_list2 = []
        # for data in portfolio['hits']['hits']:
        #     data_list2.append(data.get('_source'))
        # print('hello3',data_list2[0],len(data_list2))
        # portfolioId =[]
        # for i in data_list2:
        #     portfolioId.append(i["partner_id"])
        # print(len(list(set(portfolioId))))
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))
        if ip !='0.0.0.0':
            serializer.save(ip=ip)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChatViewSet(viewsets.ModelViewSet):
    
    queryset = Chat.objects.all().order_by("-createdAt")
    serializer_class = ChatSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields =['answer']


class SearchTextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SearchText.objects.all()
    serializer_class = SearchTextSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))
        if ip !='0.0.0.0':
            serializer.save(ip=ip)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
