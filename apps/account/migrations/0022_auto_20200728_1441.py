# Generated by Django 3.0.8 on 2020-07-28 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20200728_1427'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Business_type',
            new_name='Business',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='business_type',
            new_name='business',
        ),
    ]