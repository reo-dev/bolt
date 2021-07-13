# Generated by Django 3.0.8 on 2021-06-10 08:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_searchtext'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginlog',
            options={'verbose_name': '로그인 로그', 'verbose_name_plural': '로그인 로그'},
        ),
        migrations.AlterField(
            model_name='loginlog',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='로그인일자'),
        ),
    ]