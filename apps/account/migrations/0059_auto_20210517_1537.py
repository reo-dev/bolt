# Generated by Django 3.0.8 on 2021-05-17 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0058_partnerreviewtemp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partnerreview',
            options={'verbose_name': '파트너 리뷰', 'verbose_name_plural': '파트너 리뷰'},
        ),
        migrations.AlterModelOptions(
            name='partnerreviewtemp',
            options={'verbose_name': '파트너 임시 리뷰', 'verbose_name_plural': '파트너 임시 리뷰'},
        ),
    ]
