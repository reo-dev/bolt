# Generated by Django 2.1.1 on 2020-04-16 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_loginlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginlog',
            name='user',
        ),
        migrations.DeleteModel(
            name='LoginLog',
        ),
    ]