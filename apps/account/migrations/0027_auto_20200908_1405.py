# Generated by Django 3.0.8 on 2020-09-08 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20200908_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='is_partner',
        ),
        migrations.AlterField(
            model_name='partner',
            name='grade',
            field=models.IntegerField(choices=[(0, '파트너 X'), (1, '일반 파트너'), (2, '프리미엄 파트너')], default=0, null=True, verbose_name='파트너 등급'),
        ),
    ]
