# Generated by Django 3.0.8 on 2021-02-15 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='OrderProduct',
            new_name='orderProduct',
        ),
    ]