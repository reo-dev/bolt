from rest_framework import serializers
from apps.estimate.models import *


from django.utils import timezone
from datetime import date

now = timezone.localtime()

class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'

class DetailManufactureProcessSerializer (serializers.ModelSerializer):
    class Meta:
        model = detailManufactureProcess
        fields = '__all__'

class ManufactureProcessSerializer (serializers.ModelSerializer):
    detailmanufactureprocess_set = DetailManufactureProcessSerializer(many=True, read_only=True)
    class Meta:
        model = manufactureProcess
        fields = ['id','name', 'detailmanufactureprocess_set']

class MaterialSerializer (serializers.ModelSerializer):
    class Meta:
        model = material
        fields = '__all__'

class DetailManufactureProcessSerializer_ID_Name_Process (serializers.ModelSerializer):
    class Meta:
        model = detailManufactureProcess
        fields = ['id', 'name', 'process']

