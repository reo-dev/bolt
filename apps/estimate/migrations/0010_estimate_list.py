# Generated by Django 3.0.8 on 2021-04-14 13:08

import apps.project.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0009_auto_20210218_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_img', models.ImageField(null=True, upload_to=apps.project.models.request_update_filename, verbose_name='도면 형상 이미지')),
                ('price', models.CharField(max_length=256, null=True, verbose_name='가격정보')),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estimate.Estimate', verbose_name='도면 정보')),
            ],
            options={
                'verbose_name': '     선택한 도면 정보',
                'verbose_name_plural': '     선택한 도면 정보',
            },
        ),
    ]