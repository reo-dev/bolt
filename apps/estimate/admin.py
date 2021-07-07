#-*- coding: cp949 -*-
from django.contrib import admin
from django.db import models
from apps.estimate.models import *
from apps.account.models import *
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm
import logging
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin


@admin.register(Estimate)
class EstimatesAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']

@admin.register(manufactureProcess)
class manufactureProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(detailManufactureProcess)
class detailManufactureProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(material)
class materialAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id', 'name']


