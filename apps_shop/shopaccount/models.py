#-*- coding: cp949 -*-
from django.db import models

from apps.account.models import *

# Create your models here.

class ShopClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='쇼핑몰유저')
    address = models.CharField('주소',max_length = 150)
    phoneNumber = models.CharField('전화번호',max_length = 150)
    companyName = models.CharField('업체명',max_length = 150)
    businessNumber = models.CharField('사업자등록번호',max_length = 150)
    manager = models.CharField('담당자',max_length = 150)
    department = models.CharField('부서명',max_length = 150)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'ShopClient'
        verbose_name_plural = 'ShopClients'
