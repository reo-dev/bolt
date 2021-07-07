from django.contrib import admin
from django.db import models
from .models import *

from typing import TYPE_CHECKING

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'image', 'is_top', 'created_at']

@admin.register(Magazine_Category)
class MagazineCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']