# Generated by Django 3.0.8 on 2021-01-21 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('project', '0026_add_proposaltype_20210121_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='매니저')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='상황')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='develop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='category.Develop', verbose_name='분야'),
        ),
        migrations.AddField(
            model_name='project',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='진행상황'),
        ),
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='project.Manager', verbose_name='담당자'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='project.ProjectStatus', verbose_name='상황'),
        ),
    ]