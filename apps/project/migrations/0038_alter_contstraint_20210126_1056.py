# Generated by Django 3.0.8 on 2021-01-26 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_setnull_request_model_20210126_1348'),
    ]

    operations = [
        migrations.RunSQL(
            sql = ["ALTER TABLE project_request ADD CONSTRAINT category_fkey FOREIGN KEY (product_id) REFERENCES category_category(id) ON DELETE SET NULL"], 
            reverse_sql = ["ALTER TABLE project_request DROP CONSTRAINT category_fkey"]
        ),
    ]
