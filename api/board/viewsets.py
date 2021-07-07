#from django.contrib.auth.models import Group
from apps.board.models import *
from rest_framework import viewsets
from .serializers import *
#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.account.filters import *

class MagazineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['id','category']
    search_fields = ['title','content']

class MagazineCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Magazine_Category.objects.all()
    serializer_class = MagazineCategorySerializer
    filter_backends = [DjangoFilterBackend]