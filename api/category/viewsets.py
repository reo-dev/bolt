#-*- coding: cp949 -*-
#from django.contrib.auth.models import Group
from apps.category.models import *
from rest_framework import viewsets
from .serializers import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .paginations import *
class MaincategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Maincategory.objects.all()
    serializer_class = MaincategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['maincategory'] # �ڵ����� FK ���̺� ���� �����͸� ������ �� ����

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['category']  # �ڵ����� FK ���̺� ���� �����͸� ������ �� ����

class SubclassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Subclass.objects.all()
    serializer_class = SubclassSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['subclass']  # �ڵ����� FK ���̺� ���� �����͸� ������ �� ����

class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = CityPageNumberPagination

class DevelopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Develop.objects.all()
    serializer_class = DevelopSerializer

class DevelopbigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Developbig.objects.all().order_by('id')
    serializer_class = DevelopbigSerializer
