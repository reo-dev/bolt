#-*- coding: cp949 -*-
from django.db import models

class BigCategory(models.Model):
    title = models.CharField('카테고리명', max_length = 256)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'BigCategory'
        verbose_name_plural = 'BigCategorys'

class MiddleCategory(models.Model):
    title = models.CharField('카테고리명', max_length = 256)
    bigCategory = models.ForeignKey(BigCategory, on_delete=models.CASCADE)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'MiddleCategory'
        verbose_name_plural = 'MiddleCategorys'

class SmallCategory(models.Model):
    title = models.CharField('카테고리명', max_length = 256)
    middleCategory = models.ForeignKey(MiddleCategory, on_delete=models.CASCADE)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'SmallCategory'
        verbose_name_plural = 'SmallCategorys'
