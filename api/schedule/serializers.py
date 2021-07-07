from rest_framework import serializers
from apps.schedule.models import *


from django.utils import timezone
from datetime import date

now = timezone.localtime()


class ScheduleSerializer (serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'