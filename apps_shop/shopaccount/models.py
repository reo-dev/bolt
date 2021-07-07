#-*- coding: cp949 -*-
from django.db import models

from apps.account.models import *

# Create your models here.

class ShopClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='���θ�����')
    address = models.CharField('�ּ�',max_length = 150)
    phoneNumber = models.CharField('��ȭ��ȣ',max_length = 150)
    companyName = models.CharField('��ü��',max_length = 150)
    businessNumber = models.CharField('����ڵ�Ϲ�ȣ',max_length = 150)
    manager = models.CharField('�����',max_length = 150)
    department = models.CharField('�μ���',max_length = 150)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'ShopClient'
        verbose_name_plural = 'ShopClients'
