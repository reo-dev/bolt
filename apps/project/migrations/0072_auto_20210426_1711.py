# Generated by Django 3.0.8 on 2021-04-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0071_auto_20210426_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='check_time_client',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='클라이언트 최종 확인 시간'),
        ),
        migrations.AddField(
            model_name='answer',
            name='check_time_partner',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='클라이언트 최종 확인 시간'),
        ),
    ]
