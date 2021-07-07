# Generated by Django 3.0.8 on 2021-01-26 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category','0008_auto_20210126_1441'),
        ('account', '0043_alter_constraint_partnercategory_20210126_1127'),
    ]

    operations = [
        migrations.RunSQL(
            sql = ["UPDATE account_partnercategory SET category_id = (random()+0.01)*61;"], 
            reverse_sql = ["UPDATE account_partnercategory SET category_id = NULL;"]
        ),
    ]
