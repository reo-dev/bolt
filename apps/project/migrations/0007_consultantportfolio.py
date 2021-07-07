# Generated by Django 3.0.8 on 2021-01-06 09:58

import apps.account.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_merge_20210106_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=150, verbose_name='컨설턴트 이력')),
                ('imgPortfolio', models.ImageField(null=True, upload_to=apps.account.models.portfolio_update_filename, verbose_name='컨설턴트 포트폴리오 이미지')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Consultant', verbose_name='컨설턴트')),
            ],
        ),
    ]
