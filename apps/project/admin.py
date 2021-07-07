#-*- coding: cp949 -*-
from django.contrib import admin
from django.db import models
from apps.project.models import *
from apps.account.models import *
from apps.schedule.models import *
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm
import logging
from django.utils import timezone
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin



class ReviewInline(admin.StackedInline):
    model = Review
    can_delete = True
    extra = 0
    max_num = 15

class RequestFileInline(NestedStackedInline):
    exclude = ['request_id, id']
    model = RequestFile
    extra = 0
    fk_name = 'request'

class ScheduleInline(NestedStackedInline):
    model = Schedule
    extra = 0
    fk_name = 'request'

class RequestInline(NestedStackedInline):
    model = Request
    can_delete = False
    readonly_fields = ('project','createdAt',)
    extra = 0
    exclude = [ 'file']
    fk_name = 'project'
    inlines = [RequestFileInline,ScheduleInline]

class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = True
    raw_id_fields = ("partner",)
    #autocomplete_fields = ['partner__user']
    fields = ['partner', 'open_time', 'send_meeting', 'info_check','active']
    extra = 0
    max_num = 20

# class QuestionInline(admin.TabularInline):
#     model = Select_save
#     can_delete = True
#     extra = 0
#     max_num = 15

# 어드민페이지에서 필터 커스터마이징 하기
class DeadlineListFilter(admin.SimpleListFilter):
    title = '마감기한이 임박한 것부터'
    parameter_name='deadline'
    
    # 필터링 지정 목록 이게 사용자가 보는 리스트
    def lookups(self,request, model_admin):
        return (
            ('임박한 것부터 보기', '임박한 것부터 보기'),
        )

    # 필터링해주는 로직
    def queryset(self,request, queryset):
        currentTime = timezone.localtime()
        currentDate = currentTime.date()
        if self.value() == '임박한 것부터 보기':
            return queryset.filter(deadline__gte = currentDate).order_by('deadline')


@admin.register(Project)
class ProjectAdmin(NestedModelAdmin):
    readonly_fields = ('createdAt',)
    list_per_page =15
    list_filter = ('manager','status',DeadlineListFilter,)
    list_display = ['progressStep','createdAt','status','title','manager','reason','client_email','request']
    list_display_links =['title']
    list_editable = ['status','manager']

    def client_email(self, obj):
        if obj.client != None:
            return obj.client.user.username
        return 'none'

    def request(self, obj):
        x = Request.objects.filter(project=obj.id)
        if x:
            return x[0].name
        return 'none'

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    inlines = [RequestFileInline]
    exclude = ('file',)
    list_display = ['id', 'client', 'createdAt']
    actions = ['change_progress_0', 'change_progress_1', 'change_progress_2', 'change_progress_3']

    def change_progress_0(self, request, queryset):
        updated_count = queryset.update(progress_status='미정') #queryset.update
        self.message_user(request, '선택한 {}건의 의뢰서가 \'미정\'으로 변경되었습니다.'.format(updated_count))
    change_progress_0.short_description = "\'미정\'으로 변경하기"
   
    def change_progress_1(self, request, queryset):
        updated_count = queryset.update(progress_status='드랍') #queryset.update
        self.message_user(request, '선택한 {}건의 의뢰서가 \'드랍\'으로 변경되었습니다.'.format(updated_count))
    change_progress_1.short_description = "\'드랍\'으로 변경하기"
        
    def change_progress_2(self, request, queryset):
        updated_count = queryset.update(progress_status='진행중') #queryset.update
        self.message_user(request, '선택한 {}건의 의뢰서가 \'진행중\'으로 변경되었습니다.'.format(updated_count))
    change_progress_2.short_description = "\'진행중\'로 변경하기"
    
    def change_progress_3(self, request, queryset):
        updated_count = queryset.update(progress_status='전환') #queryset.update
        self.message_user(request, '선택한 {}건의 의뢰서가 \'전환\'으로 변경되었습니다.'.format(updated_count))
    change_progress_3.short_description = "\'전환\'로 변경하기"

# # @admin.register(RequestFile)
# class RequestFileAdmin (admin.ModelAdmin):
#     list_display = ['id', 'request', 'file']
    
# # @admin.register(Select_save)
# class Select_saveAdmin(admin.ModelAdmin):
#     list_display = ['id', 'category', 'request', 'question', 'answer']

# @admin.register(Select)
# class SelectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'category', 'request']

# @admin.register(Content)
# class SelectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'request', 'content1', 'content2', 'content3', 'content4']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['partner_phone', 'request_name', 'partner']

    def partner_phone(self, obj):
        partner = obj.partner
        phone = User.objects.get(username=partner).phone
        return phone

    def request_name(self, obj):
        project_id = obj.project
        request_name = Request.objects.get(project = project_id)
        return request_name

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'project','title','content','createdAt']



# @admin.register(KakaoToken)
# class KakaoTokenAdmin(admin.ModelAdmin):
#     list_display = ['id', 'token']

# @admin.register(ProjectStatus)
# class ProjectStatusAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']

# 어드민페이지에서 액션 지정해주기
def createRecomment(modeladmin, request, queryset):
    user = User.objects.get(username= "client_test@naver.com")
    for obj in queryset:
        Comment.objects.create(
            client = Client.objects.get(user=user),
            project = obj.project
        )
createRecomment.short_description = "해당 요청사항에 대한 답변 남기기"

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'client','project','content','createdAt']
#     # 위에서 만든 함수 지정
#     actions = [createRecomment]
