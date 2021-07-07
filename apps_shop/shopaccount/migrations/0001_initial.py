# Generated by Django 3.0.8 on 2021-02-15 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='주소')),
                ('phoneNumber', models.CharField(max_length=150, verbose_name='전화번호')),
                ('companyName', models.CharField(max_length=150, verbose_name='업체명')),
                ('businessNumber', models.CharField(max_length=150, verbose_name='사업자등록번호')),
                ('manager', models.CharField(max_length=150, verbose_name='담당자')),
                ('department', models.CharField(max_length=150, verbose_name='부서명')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='쇼핑몰유저')),
            ],
            options={
                'verbose_name': 'ShopClient',
                'verbose_name_plural': 'ShopClients',
            },
        ),
    ]
