# Generated by Django 3.0.8 on 2021-01-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_comment_update_20210113_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='showName',
            field=models.CharField(default='default', max_length=256, verbose_name='세부일정보여주기용'),
        ),
    ]
