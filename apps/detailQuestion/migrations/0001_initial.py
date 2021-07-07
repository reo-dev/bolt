# Generated by Django 3.0.8 on 2021-01-12 02:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0013_proposaltype_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailQuestionTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='질문제목')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='작성일')),
            ],
            options={
                'verbose_name': '     질문제목',
                'verbose_name_plural': '     질문제목',
            },
        ),
        migrations.CreateModel(
            name='DetailQuestionSelect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select', models.TextField(verbose_name='질문 선택지')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='작성일')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detailQuestion.DetailQuestionTitle', verbose_name='질문제목')),
            ],
        ),
        migrations.CreateModel(
            name='DetailQuestionSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='작성일')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detailQuestion.DetailQuestionTitle', verbose_name='질문제목')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Request', verbose_name='의뢰서')),
                ('select', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detailQuestion.DetailQuestionSelect', verbose_name='질문 선택지')),
            ],
        ),
    ]
