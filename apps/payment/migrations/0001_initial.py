# Generated by Django 2.1.1 on 2020-04-14 02:29

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
            name='Paylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_uid', models.CharField(max_length=256, verbose_name='결제정보')),
                ('product_name', models.CharField(max_length=256, verbose_name='상품명')),
                ('channel', models.CharField(max_length=256, verbose_name='결제환경(웹/모바일')),
                ('pay_method', models.CharField(max_length=256, verbose_name='결제 방법(카드/휴대폰 등)')),
                ('status', models.CharField(max_length=256, verbose_name='결제성공여부')),
                ('product_price', models.IntegerField(default=0, verbose_name='비용')),
                ('coin', models.IntegerField(default=0, verbose_name='코인')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '     결제저장',
                'verbose_name_plural': '     결제저장',
            },
        ),
    ]
