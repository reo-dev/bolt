# Generated by Django 3.0.8 on 2021-02-18 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paylist',
            old_name='coin',
            new_name='count',
        ),
    ]