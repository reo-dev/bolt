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
        # imgUpload.fileupload()
        # elastic.send()
        
        es = Elasticsearch([{'host':'localhost','port':'9200'}])
        docs = es.search(
            index='test',
            body={
                "query": {
                    "multi_match": {
                        "query": '볼트',
                        "fields": [
                            "name", 
                            "info_company"
                        ]
                    }
                }
            })
        
        print('hello2',docs)

        data_list = []
        for data in docs['hits']['hits']:
            data_list.append(data.get('_source'))
        print('hello3',data_list[0])

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
