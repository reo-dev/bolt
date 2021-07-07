#-*- coding: cp949 -*-
from django.db import models
from apps.project.models import *

# Create your models here.
# ------------------------------------------------------------------
# Model   : Schedule
# Description : 스케쥴
# ------------------------------------------------------------------
class Schedule(models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name = '의뢰서', null = True)
    startAt = models.DateTimeField('시작시각')
    endAt = models.DateTimeField('종료시각')
    createdAt = models.DateTimeField('생성일', auto_now_add = True)
    note = models.TextField('메모', null =  True)
    status = models.BooleanField('상태')
    isOnline = models.BooleanField('온라인미팅', default = False, null = False)

    class Meta:
        verbose_name = '     스케쥴'
        verbose_name_plural = '     스케쥴'
    def __str__(self):
        return str(self.id)
