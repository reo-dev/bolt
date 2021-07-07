# Generated by Django 3.0.8 on 2021-02-10 06:50

from django.db import migrations
from api.account.serializers import *
from ..models import *

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0050_add_department_20210208_1152'),
    ]

    
    def changePartnerLogo(apps, schema_editor):
        i = 1
        partnerList = Partner.objects.filter(logo='null')
        for partner in partnerList:
            if i == 568:
                break
            partner.logo = "partner/" + str(i) +".png"
            partner.save()
            i += 1


    operations = [
        migrations.RunPython(changePartnerLogo, reverse_code = migrations.RunPython.noop),
    ]
