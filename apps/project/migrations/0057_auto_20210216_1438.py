# Generated by Django 3.0.8 on 2021-02-16 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0056_auto_20210216_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='프로젝트'),
        ),
    ]
