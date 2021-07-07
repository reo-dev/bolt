#-*- coding: cp949 -*-
from django.db import models

# Create your models here.

# ------------------------------------------------------------------
# Model   : kakao
# Description : 카카오톡 모델
# ------------------------------------------------------------------
class Sendkakao(models.Model):
    status_code = models.IntegerField('메세지 전송결과', default=0)
    description = models.CharField('메세지 전송 결과 상세', null=True, max_length = 100)
    refkey = models.CharField('레퍼런스키', null=True, max_length = 100)
    messagekey = models.CharField('메세지키', null=True, max_length = 100)

    class Meta:
        verbose_name = '     카카오톡'
        verbose_name_plural = '     카카오톡'

    def __str__(self):
        return str(self.id)
