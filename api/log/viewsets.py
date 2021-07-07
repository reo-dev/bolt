from rest_framework import (
    viewsets,
    status,
    mixins,
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.log.models import *
from .serializers import *

class ClickLogViewSet (viewsets.ModelViewSet):
    serializer_class = ClickLogSerializer
    queryset = clickLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']




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
        request.data.ip=ip
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(ip=self.request.META['REMOTE_ADDR'])
