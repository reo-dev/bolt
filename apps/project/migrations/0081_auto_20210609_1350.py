# Generated by Django 3.0.8 on 2021-06-09 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0080_project_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chat_type',
            field=models.IntegerField(choices=[(0, '텍스트'), (1, '이미지'), (2, '파일')], null=True, verbose_name='채팅 타입'),
        ),
    ]