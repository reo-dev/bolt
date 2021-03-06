# Generated by Django 2.1.1 on 2020-04-14 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP_ADDRESS')),
                ('user_agent', models.CharField(max_length=300, verbose_name='HTTP User Agent')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('log_type', models.CharField(max_length=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='login_logs', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'user_login_log',
                'verbose_name_plural': 'user_login_logs',
                'ordering': ('-created_at',),
            },
        ),
    ]
