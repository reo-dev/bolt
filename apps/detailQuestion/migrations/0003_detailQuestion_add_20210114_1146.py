# Generated by Django 3.0.8 on 2021-01-14 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detailQuestion', '0002_detailQuestion_data_20210113_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailquestionselect',
            name='nextTitle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nextTitle', to='detailQuestion.DetailQuestionTitle', verbose_name='다음 질문제목'),
        ),
        migrations.AlterField(
            model_name='detailquestionselect',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title', to='detailQuestion.DetailQuestionTitle', verbose_name='질문제목'),
        ),
    ]
