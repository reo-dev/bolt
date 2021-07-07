from django.contrib import admin
from django.db import models
from apps.payment.models import *



@admin.register(Paylist)
class PaylistAdmin(admin.ModelAdmin):
     list_display = ['id', 'merchant_uid', 'user', 'status']