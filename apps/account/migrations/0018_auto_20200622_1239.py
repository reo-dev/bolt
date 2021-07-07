# Generated by Django 2.1.1 on 2020-06-22 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientclass',
            name='name',
        ),
        migrations.RemoveField(
            model_name='clientclass',
            name='title',
        ),
        migrations.AddField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=256, null=True, verbose_name='업체명'),
        ),
        migrations.AddField(
            model_name='client',
            name='path',
            field=models.CharField(max_length=256, null=True, verbose_name='방문경로'),
        ),
        migrations.AddField(
            model_name='client',
            name='title',
            field=models.CharField(max_length=256, null=True, verbose_name='직급'),
        ),
    ]
