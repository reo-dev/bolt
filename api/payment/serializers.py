from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.payment.models import *
from apps.account.models import *
from api.account.serializers import *

class PaylistSerializer(serializers.ModelSerializer):
    user = PatchUserSerializer()
    class Meta:
        model = Paylist
        fields = ['id','user', 'merchant_uid', 'status', 'product_price', 'count', 'channel', 'pay_method' ]




