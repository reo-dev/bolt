# Generated by Django 3.0.8 on 2021-01-13 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_kakaotoken_20210113_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='fieldName',
            new_name='content',
        ),
    ]