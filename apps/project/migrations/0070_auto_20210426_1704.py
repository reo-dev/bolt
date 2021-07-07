# Generated by Django 3.0.8 on 2021-04-26 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0069_auto_20210426_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='check_time_partner',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='파트너 제안서 최종 확인 시간'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='check_time_client',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='클라이언트 제안서 최종 확인 시간'),
        ),
    ]
