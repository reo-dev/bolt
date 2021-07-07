#-*- coding: cp949 -*-
from django.db import models

from apps_shop.shopcategory.models import *
from apps_shop.shopaccount.models import *

class Product(models.Model):
    name = models.CharField(max_length = 256)
    thumbnailImage = models.ImageField(upload_to=None)
    mainImage = models.ImageField(upload_to=None)
    explain = models.TextField()
    stockQuantity = models.IntegerField('재고수량')
    bigCategory = models.ForeignKey(BigCategory, on_delete=models.CASCADE)
    middleCategory = models.ForeignKey(MiddleCategory, on_delete=models.CASCADE)
    smallCategory = models.ForeignKey(SmallCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '     상품'
        verbose_name_plural = '     상품'

class Order(models.Model):
    client = models.ForeignKey(ShopClient, on_delete=models.CASCADE)
    option = models.CharField('구매옵션',max_length = 256)
    request = models.TextField()
    orderDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField('주문상태',max_length = 256)
    orderProduct = models.ManyToManyField(Product, related_name='orders', through = 'OrderProduct')

    def __str__(self):
        pass

    class Meta:
        verbose_name = '     주문'
        verbose_name_plural = '     주문'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    orderPrice = models.CharField('주문가격', max_length = 256)

    def __str__(self):
        pass

    class Meta:
        verbose_name = '     주문상품'
        verbose_name_plural = '     주문상품'

class Cart(models.Model):
    client = models.ForeignKey(ShopClient, on_delete=models.CASCADE)
    
    def __str__(self):
        pass

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

class RegularOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    nextPayment = models.DateTimeField('다음 결제일',auto_now=False, auto_now_add=False)
    paymentPeriod = models.CharField('결제주기', max_length = 256)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'Regular'
        verbose_name_plural = 'Regulars'
