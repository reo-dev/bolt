from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id','startAt','endAt','createdAt', 'request', 'status', 'note', 'isOnline']

