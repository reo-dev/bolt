# Generated by Django 3.0.8 on 2021-01-18 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0040_copyTablesql_20210114_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='showPassword',
            field=models.CharField(default='null', max_length=256, verbose_name='보여줄패스워드'),
        ),
    ]
