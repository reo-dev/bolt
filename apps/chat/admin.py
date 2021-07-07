from django.contrib import admin
from apps.project.models import *
import csv
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin



# @admin.register(Chat)
# class ChatAdmin(admin.ModelAdmin):
#     list_display = ['id','text_content','answer','user_type', 'createdAt','chat_type']
#     actions = ['export_as_csv']
