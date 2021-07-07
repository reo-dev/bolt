#-*- coding: cp949 -*-
from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

# excel
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

from .models import *
from apps.project.models import *
from apps.log.models import *
# Register your models here.

from django.forms import TextInput, Textarea
from django.db import models

from typing import TYPE_CHECKING

import csv
from django.http import HttpResponse

from dateutil.relativedelta import relativedelta
import sys


class PortfolioInline(admin.StackedInline):
    model = Portfolio
    can_delete = True
    extra = 0
    max_num = 15

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(User)
class UserAdmin(ImportExportMixin,admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id','username', 'date_joined','type', 'partner_name', 'phone','marketing','last_activity','login_count','half_months_count','one_months_count','three_months_count','been_half_months_count','been_one_months_count','been_three_months_count']
    actions = ['export_as_csv']
    search_fields = ['phone']
    # list_per_page = sys.maxsize

    # a=0
    # b=0

    def partner_name(self, obj):
        if(obj.type == 1):
            partner_name = Partner.objects.get(user=obj.id).name
            return partner_name

    def login_count(self, obj):

        cnt = len(LoginLog.objects.filter(user=obj.id))
        return cnt
    login_count.short_description='로그인 카운트'

    def half_months_count(self, obj):

        today_=datetime.datetime.today()
        new_date = today_ + relativedelta(days=-15)
        cnt = len(LoginLog.objects.filter(user=obj.id).filter(created_at__gte=str(new_date)))
        return cnt
    half_months_count.short_description='최근 15일간 로그인'

    def one_months_count(self, obj):

        today_=datetime.datetime.today()
        new_date = today_ + relativedelta(months=-1)
        cnt = len(LoginLog.objects.filter(user=obj.id).filter(created_at__gte=str(new_date)))
        return cnt
    one_months_count.short_description='최근 1개월 로그인'

    def three_months_count(self, obj):

        today_=datetime.datetime.today()
        new_date = today_ + relativedelta(months=-3)
        cnt = len(LoginLog.objects.filter(user=obj.id).filter(created_at__gte=str(new_date)))
        return cnt
    three_months_count.short_description='최근 3개월 로그인'

    def been_half_months_count(self, obj):
        cnt=0
        x = LoginLog.objects.filter(user=obj.id)
        for i in range(len(x)-1):
            if x[i].created_at+relativedelta(days=-15) > x[i+1].created_at:
                cnt+=1
        return cnt
    been_half_months_count.short_description='15일 만에 로그인'

    def been_one_months_count(self, obj):
        cnt=0
        x = LoginLog.objects.filter(user=obj.id)
        for i in range(len(x)-1):
            if x[i].created_at+relativedelta(months=-1) > x[i+1].created_at:
                cnt+=1
        return cnt
    been_one_months_count.short_description='1개월 만에 로그인'

    def been_three_months_count(self, obj):
        cnt=0
        x = LoginLog.objects.filter(user=obj.id)
        for i in range(len(x)-1):
            if x[i].created_at+relativedelta(months=-3) > x[i+1].created_at:
                cnt+=1
        return cnt
    been_three_months_count.short_description='3개월 만에 로그인'

    # def months_count(self, obj):
        
    #     # a_ = User.objects.filter(type=0)
    #     # m=len(a_)
    #     # b_ = User.objects.filter(type=1)
    #     # f=len(b_)
    #     cnt=0
    #     x = LoginLog.objects.filter(user=obj.id)
    #     for i in range(len(x)-1):
    #         if x[i].created_at+relativedelta(months=-3) > x[i+1].created_at:
    #             cnt+=1
    #     try:
    #         if x[0].type==0:
    #             UserAdmin.a+=cnt
    #         else:
    #             UserAdmin.b+=cnt
    #     except:
    #         pass
    #     print(UserAdmin.a,UserAdmin.b)
    #     return 0



@admin.register(Client)
class ClientAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','client_phone', 'client_email', 'name', 'title','business', 'path', 'marketing','client_signup_date',
                        'request_count', 'latest_request']
    actions = ['export_as_csv']
    
    def client_phone(self, obj):
        phone = User.objects.get(username=obj.user).phone
        return phone

    def client_email(self, obj):
        email = User.objects.get(username=obj.user).username
        return email

    def marketing(self, obj):
        marketing = User.objects.get(username=obj.user).marketing
        if marketing ==True:
            return 'O'
        return 'X'

    def client_signup_date(self, obj):
        return obj.user.date_joined

        client_signup_date.short_descrption = "°¡??????"

    def request_count(self, obj):
        request = Request.objects.filter(client=obj)
        count = len(request)
        return count

        request_count.short_descrption = "??·?¼­ ¼?"

    def latest_request(self, obj):
        request = Request.objects.filter(client=obj).order_by('-createdAt')
        latest_request = request.first()
        return latest_request

        latest_request.short_descrption = "??±? ??·?"

@admin.register(Partner)
class PartnerAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id', 'partner_phone', 'partner_email', 'name', 'city']
    search_fields = ['name','history','category_middle__category','info_company']


    def partner_phone(self, obj):
        phone = User.objects.get(username=obj.user).phone
        return phone

    def partner_email(self, obj):
        email = User.objects.get(username=obj.user).username
        return email

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ['id','path']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['id','business']


@admin.register(PartnerReview)
class PartnerReviewAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(PartnerReviewTemp)
class PartnerReviewAdmin(admin.ModelAdmin):
    list_display = ['id']
