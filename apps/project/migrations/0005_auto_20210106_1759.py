# Generated by Django 3.0.8 on 2021-01-06 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_merge_20210106_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultant',
            options={'verbose_name': '     컨설턴트', 'verbose_name_plural': '     컨설턴트'},
        ),
        migrations.AlterModelOptions(
            name='proposal',
            options={'verbose_name': '     견적서', 'verbose_name_plural': '     견적서'},
        ),
        migrations.AlterModelOptions(
            name='proposaltype',
            options={'verbose_name': '     견적서타입', 'verbose_name_plural': '     견적서타입'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': '     세부일정', 'verbose_name_plural': '     세부일정'},
        ),
    ]
