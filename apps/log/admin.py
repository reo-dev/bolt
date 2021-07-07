from django.contrib import admin
from apps.log.models import *
import csv
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin


# Register your models here.
@admin.register(clickLog)
class clickLogAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id', 'client','search','partner','created_at']
    actions = ['export_as_csv']


@admin.register(Chat)
class ChatAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','text_content','answer','user_type', 'createdAt','chat_type']
    actions = ['export_as_csv']


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['id','user','type','created_at']

@admin.register(SearchText)
class SearchTextAdmin(admin.ModelAdmin):
    list_display = ['id','ip','text','search_data_cnt','percent_success_search']
    
    def search_data_cnt(self, obj):
        x=Partner.objects.filter(user__is_active=True).filter(Q(name__contains=obj.text) | Q(info_company__contains=obj.text) | Q(history__contains=obj.text) | Q(category_middle__category__contains=obj.text)).order_by('user_id').distinct()
        return len(x)
    search_data_cnt.short_description='Number of Partner'

    def percent_success_search(self, obj):
        x=Partner.objects.filter(user__is_active=True).filter(Q(name__contains=obj.text) | Q(info_company__contains=obj.text) | Q(history__contains=obj.text) | Q(category_middle__category__contains=obj.text)).order_by('user_id').distinct()
        if len(x) >= 3:
            return True
        else:
            return False
    percent_success_search.short_description='Search Success'



# 276@276.com
# 364@364.com
# 96@96.com
# 20@20.com
# 190@190.com
# 191@191.com
# 220@220.com
# 138@138.com
# chydream@chol.com



# class PartnerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     #orderbyList = ['-avg_score', '-id']
#     queryset = Partner.objects.filter(user__is_active=True).order_by('-id')
#     serializer_class = PartnerSerializer
#     pagination_class = PartnerPageNumberPagination
#     filter_backends = [filters.SearchFilter,PartnerFilter, filters.OrderingFilter]
#     filterset_fields = ['history','history_set', 'city', 'category_middle__id', 'history_set__id', 'answer_set__id']
#     search_fields = ['name', 'info_company','history','category_middle__category']
#     ordering_fields = '__all__'
