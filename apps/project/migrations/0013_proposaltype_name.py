# Generated by Django 3.0.8 on 2021-01-08 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_project_proposal_20210108_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposaltype',
            name='name',
            field=models.CharField(default='수정하세요', max_length=150, verbose_name='견적서타입이름'),
        ),
    ]