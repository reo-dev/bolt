# Generated by Django 3.0.8 on 2021-01-29 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0045_client_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='showPassword',
        ),
    ]