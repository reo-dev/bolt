# Generated by Django 3.0.8 on 2021-02-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0008_material_data_20210210_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='process',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='프로세스'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='maxPrice',
            field=models.FloatField(default=0, verbose_name='서출최대가격'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='minPrice',
            field=models.FloatField(default=0, verbose_name='사출최소가격'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='totalMaxPrice',
            field=models.FloatField(default=0, verbose_name='금형 사출 최대 가격'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='totalMinPrice',
            field=models.FloatField(default=0, verbose_name='금형 사출 최소 가격 '),
        ),
    ]
