# Generated by Django 3.0.8 on 2021-01-21 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_add_manager_20210121_1707'),
        ('category','0002_auto_20210121_1716'),
    ]

    operations = [
        migrations.RunSQL(
            sql = ["UPDATE project_project SET develop_id=15;UPDATE project_project SET manager_id=1;UPDATE project_project SET project_status_id=1"], 
            reverse_sql = ["UPDATE project_project SET develop_id=null;UPDATE project_project SET manager_id=null;UPDATE project_project SET project_status_id=null"]
        ),
    ]
