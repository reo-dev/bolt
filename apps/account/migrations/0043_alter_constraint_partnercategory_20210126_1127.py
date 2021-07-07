# Generated by Django 3.0.8 on 2021-01-26 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project','0039_setnull_request_20210126_1326'),
        ('account', '0042_auto_20210126_1325'),
    ]

    operations = [
        migrations.RunSQL(
            sql = ["ALTER TABLE account_partnercategory DROP CONSTRAINT account_partnercateg_category_id_acfe9ec4_fk_category_ ,ADD CONSTRAINT category_fkey FOREIGN KEY (category_id) REFERENCES category_category(id) ON DELETE SET NULL"], 
            reverse_sql = ["ALTER TABLE account_partnercategory DROP CONSTRAINT category_fkey,ADD CONSTRAINT account_partnercateg_category_id_acfe9ec4_fk_category_ FOREIGN KEY (category_id) REFERENCES category_category(id)"]
        ),
        
    ]
