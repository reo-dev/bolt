# Generated by Django 3.0.8 on 2021-02-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_category_additionalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='additionalPrice',
            field=models.CharField(default='0', max_length=256, null=True, verbose_name='추가금액'),
        ),
    ]