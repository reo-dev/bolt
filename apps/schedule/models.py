#-*- coding: cp949 -*-
from django.db import models
from apps.project.models import *

# Create your models here.
# ------------------------------------------------------------------
# Model   : Schedule
# Description : ������
# ------------------------------------------------------------------
class Schedule(models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name = '�Ƿڼ�', null = True)
    startAt = models.DateTimeField('���۽ð�')
    endAt = models.DateTimeField('����ð�')
    createdAt = models.DateTimeField('������', auto_now_add = True)
    note = models.TextField('�޸�', null =  True)
    status = models.BooleanField('����')
    isOnline = models.BooleanField('�¶��ι���', default = False, null = False)

    class Meta:
        verbose_name = '     ������'
        verbose_name_plural = '     ������'
    def __str__(self):
        return str(self.id)
