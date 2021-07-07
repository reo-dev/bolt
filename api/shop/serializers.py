from rest_framework import serializers
from apps_shop.shop.models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','client','option','request','orderDate','status','orderProduct']
