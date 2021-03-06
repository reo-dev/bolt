# Generated by Django 3.0.8 on 2021-04-19 08:48

import apps.project.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0066_answer_createdat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='file',
        ),
        migrations.AddField(
            model_name='request',
            name='deadline_state',
            field=models.CharField(choices=[('납기일미정', '납기일미정'), ('납기일협의가능', '납기일협의가능')], default='', max_length=10, verbose_name='납기일 상태'),
        ),
        migrations.AddField(
            model_name='request',
            name='file_close',
            field=models.FileField(blank=True, null=True, upload_to=apps.project.models.request_update_filename, verbose_name='비공개파일'),
        ),
        migrations.AddField(
            model_name='request',
            name='file_open',
            field=models.FileField(blank=True, null=True, upload_to=apps.project.models.request_update_filename, verbose_name='공개파일'),
        ),
        migrations.AddField(
            model_name='request',
            name='request_state',
            field=models.CharField(choices=[('상담요청', '상담요청'), ('견적문의', '견적문의'), ('업체수배', '업체수배')], default='', max_length=10, verbose_name='문의 목적'),
        ),
        migrations.AlterField(
            model_name='request',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='상담명'),
        ),
    ]
