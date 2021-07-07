#-*- coding: cp949 -*-
from django.db import models
from django.utils import timezone
from apps.project.models import *

# 해당 모델은 현재 사용하고 있지 않음. 의뢰에 대한 객관식 질문을 제공하기 위함이나 그에 대한 내용이 정제되지 않아 주관식으로 작성할 예정이며, 추후 정립이 된 상태에는 객관식 모델을
# 다시 사용할 수 있음

# ------------------------------------------------------------------
# Model   : detailQuestionTitle
# Description : 제품정보 질문 제목(내용)
# ------------------------------------------------------------------
class DetailQuestionTitle(models.Model):
    question = models.TextField('질문제목', blank = False, null = False)
    createdAt = models.DateTimeField('작성일', default = timezone.now)

    class Meta:
        verbose_name = '     질문제목'
        verbose_name_plural = '     질문제목'

    def __str__(self):
        return str(self.question)

class DetailQuestionSelect(models.Model):
    title = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '질문제목', null = False, related_name = 'title')
    select = models.TextField('질문 선택지', null = False)
    nextTitle = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '다음 질문제목', null = True, related_name = 'nextTitle')
    createdAt = models.DateTimeField('작성일', default = timezone.now)

    def __str__(self):
        return str(self.select)

class DetailQuestionSave (models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name = '의뢰서', null = False)
    question = models.ForeignKey(DetailQuestionTitle, on_delete = models.CASCADE, verbose_name = '질문제목', null = False)
    select = models.ForeignKey(DetailQuestionSelect, on_delete = models.CASCADE, verbose_name = '질문 선택지', null = False)
    createdAt = models.DateTimeField('작성일', default = timezone.now)