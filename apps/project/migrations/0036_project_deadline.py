# Generated by Django 3.0.8 on 2021-01-22 05:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_update_type_task_20210122_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='기한'),
        ),
    ]