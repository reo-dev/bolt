# Generated by Django 3.0.8 on 2021-01-21 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_add_status_data_20210121_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manager',
            options={'verbose_name': '     프로젝트매니저', 'verbose_name_plural': '     프로젝트매니저'},
        ),
        migrations.AlterModelOptions(
            name='projectstatus',
            options={'verbose_name': '     프로젝트진행상황', 'verbose_name_plural': '     프로젝트진행상황'},
        ),
    ]
