#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from apps.account.models import *

from hashids import Hashids

# ------------------------------------------------------------------
# Model   : Paylist
# Description : 결제 저장 모델
# ------------------------------------------------------------------

class Paylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_uid = models.CharField('결제정보', max_length=256)
    product_name = models.CharField('상품명', max_length=256)
    #buyer_email = models.CharField('구매자 이메일', max_length=256)
    #buyer_name = models.CharField('구매자 이름', max_length=256)
    #buyer_tel = models.CharField('구매자 전화번호', max_length=256)
    channel = models.CharField('결제환경(웹/모바일', max_length=256)
    pay_method = models.CharField('결제 방법(카드/휴대폰 등)', max_length=256)
    status = models.CharField('결제성공여부', max_length=256)
    product_price = models.IntegerField('비용', default=0)
    count = models.IntegerField('개수', default=0, null = True)

    class Meta:
        verbose_name = '     결제저장'
        verbose_name_plural = '     결제저장'

    def __str__(self):
        return str(self.id)