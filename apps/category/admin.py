from django.contrib import admin
from django.db import models
from .models import *

@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
        list_display = ['id', 'maincategory']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        list_display = ['id', 'maincategory', 'category','additionalPrice']

@admin.register(Subclass)
class SubclassAdmin(admin.ModelAdmin):
        list_display = ['id', 'maincategory', 'category', 'subclass']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
        list_display = ['id', 'city']

@admin.register(Developbig)
class ProductbigAdmin(admin.ModelAdmin):
        list_display = ['id', 'maincategory']

@admin.register(Develop)
class ProductAdmin(admin.ModelAdmin):
        list_display = ['id', 'maincategory', 'category', 'coin']