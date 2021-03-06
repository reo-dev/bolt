# Generated by Django 3.0.8 on 2021-04-14 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0055_auto_20210414_2208'),
        ('project', '0064_auto_20210413_1643'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Common',
        ),
        migrations.RemoveField(
            model_name='consultantportfolio',
            name='consultant',
        ),
        migrations.RemoveField(
            model_name='projectfile',
            name='project',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='consultant',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='project',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='proposalType',
        ),
        migrations.RemoveField(
            model_name='proposaltype',
            name='task',
        ),
        migrations.RemoveField(
            model_name='request_parts',
            name='request',
        ),
        migrations.RemoveField(
            model_name='reuqest_parts_list',
            name='id',
        ),
        migrations.RemoveField(
            model_name='request',
            name='product_inform',
        ),
        migrations.AddField(
            model_name='answer',
            name='share_inform',
            field=models.BooleanField(default=False, verbose_name='정보 공개 체크'),
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Client', verbose_name='작성클라이언트'),
        ),
        migrations.AddField(
            model_name='request',
            name='price',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='희망비용'),
        ),
        migrations.AddField(
            model_name='requestfile',
            name='share_inform',
            field=models.BooleanField(default=False, verbose_name='정보 공개 체크'),
        ),
        migrations.DeleteModel(
            name='Consultant',
        ),
        migrations.DeleteModel(
            name='ConsultantPortfolio',
        ),
        migrations.DeleteModel(
            name='ProjectFile',
        ),
        migrations.DeleteModel(
            name='Proposal',
        ),
        migrations.DeleteModel(
            name='ProposalType',
        ),
        migrations.DeleteModel(
            name='Request_parts',
        ),
        migrations.DeleteModel(
            name='Reuqest_parts_list',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
