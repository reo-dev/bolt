# Generated by Django 3.0.8 on 2021-02-01 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0046_remove_user_showpassword'),
        ('project', '0045_remove_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': '리뷰', 'verbose_name_plural': '리뷰'},
        ),
        migrations.AlterField(
            model_name='review',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Client', verbose_name='작성클라이언트'),
        ),
        migrations.AlterField(
            model_name='review',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너'),
        ),
        migrations.AlterField(
            model_name='review',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='프로젝트'),
        ),
    ]
