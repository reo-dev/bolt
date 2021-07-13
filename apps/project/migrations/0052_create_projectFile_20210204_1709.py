# Generated by Django 3.0.8 on 2021-02-04 08:09

import apps.project.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0051_add_consultant_20210203_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to=apps.project.models.project_update_filename, verbose_name='프로젝트 파일')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='프로젝트')),
            ],
            options={
                'verbose_name': '     제품 기본정보 첨부파일',
                'verbose_name_plural': '     제품 기본정보 첨부파일',
            },
        ),
    ]