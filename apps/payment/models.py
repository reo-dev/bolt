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
# Description : ���� ���� ��
# ------------------------------------------------------------------

class Paylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_uid = models.CharField('��������', max_length=256)
    product_name = models.CharField('��ǰ��', max_length=256)
    #buyer_email = models.CharField('������ �̸���', max_length=256)
    #buyer_name = models.CharField('������ �̸�', max_length=256)
    #buyer_tel = models.CharField('������ ��ȭ��ȣ', max_length=256)
    channel = models.CharField('����ȯ��(��/�����', max_length=256)
    pay_method = models.CharField('���� ���(ī��/�޴��� ��)', max_length=256)
    status = models.CharField('������������', max_length=256)
    product_price = models.IntegerField('���', default=0)
    count = models.IntegerField('����', default=0, null = True)

    class Meta:
        verbose_name = '     ��������'
        verbose_name_plural = '     ��������'

    def __str__(self):
        return str(self.id)