# Generated by Django 3.0.8 on 2021-02-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0062_remove_proposaltype_additionalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='피드백'),
        ),
        migrations.AlterField(
            model_name='project',
            name='progressStep',
            field=models.CharField(choices=[('정보입력', '정보입력'), ('세부질문', '세부질문'), ('상담신청', '상담신청')], default='', max_length=10, verbose_name='고객 진행 단계'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('상', '상'), ('중상', '중상'), ('중', '중'), ('중하', '중하'), ('하', '하')], default='미정', max_length=10, null=True, verbose_name='전환가능성'),
        ),
    ]
