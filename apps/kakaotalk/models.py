#-*- coding: cp949 -*-
from django.db import models

# Create your models here.

# ------------------------------------------------------------------
# Model   : kakao
# Description : īī���� ��
# ------------------------------------------------------------------
class Sendkakao(models.Model):
    status_code = models.IntegerField('�޼��� ���۰��', default=0)
    description = models.CharField('�޼��� ���� ��� ��', null=True, max_length = 100)
    refkey = models.CharField('���۷���Ű', null=True, max_length = 100)
    messagekey = models.CharField('�޼���Ű', null=True, max_length = 100)

    class Meta:
        verbose_name = '     īī����'
        verbose_name_plural = '     īī����'

    def __str__(self):
        return str(self.id)
