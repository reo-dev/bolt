#-*- coding: cp949 -*-
from django.db import models
from django.utils import timezone
from apps.project.models import *

# �ش� ���� ���� ����ϰ� ���� ����. �Ƿڿ� ���� ������ ������ �����ϱ� �����̳� �׿� ���� ������ �������� �ʾ� �ְ������� �ۼ��� �����̸�, ���� ������ �� ���¿��� ������ ����
# �ٽ� ����� �� ����

# ------------------------------------------------------------------
# Model   : detailQuestionTitle
# Description : ��ǰ���� ���� ����(����)
# ------------------------------------------------------------------
class DetailQuestionTitle(models.Model):
    question = models.TextField('��������', blank = False, null = False)
    createdAt = models.DateTimeField('�ۼ���', default = timezone.now)

    class Meta:
        verbose_name = '     ��������'
        verbose_name_plural = '     ��������'

    def __str__(self):
        return str(self.question)

class DetailQuestionSelect(models.Model):
    title = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '��������', null = False, related_name = 'title')
    select = models.TextField('���� ������', null = False)
    nextTitle = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '���� ��������', null = True, related_name = 'nextTitle')
    createdAt = models.DateTimeField('�ۼ���', default = timezone.now)

    def __str__(self):
        return str(self.select)

class DetailQuestionSave (models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name = '�Ƿڼ�', null = False)
    question = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '��������', null = False)
    select = models.ForeignKey(DetailQuestionSelect, on_delete = models.CASCADE, verbose_name = '���� ������', null = False)
    createdAt = models.DateTimeField('�ۼ���', default = timezone.now)