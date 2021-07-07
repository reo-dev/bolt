# Generated by Django 3.0.8 on 2021-06-18 01:53

import apps.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0062_delete_searchtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=256, null=True, verbose_name='파일이름')),
                ('partner_info_file', models.FileField(blank=True, max_length=255, null=True, upload_to=apps.account.models.partner_update_filename, verbose_name='파트너정보 파일')),
                ('portfolio_file', models.FileField(blank=True, max_length=255, null=True, upload_to=apps.account.models.partner_update_filename, verbose_name='포트폴리오 파일')),
            ],
            options={
                'verbose_name': '파일이름',
                'verbose_name_plural': '파일이름',
            },
        ),
        migrations.AlterField(
            model_name='partner',
            name='real_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='실제 휴대폰 번호'),
        ),
    ]
