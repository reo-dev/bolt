# Generated by Django 3.0.8 on 2020-09-08 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_auto_20200908_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='grade',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True, verbose_name='파트너 등급'),
        ),
    ]
