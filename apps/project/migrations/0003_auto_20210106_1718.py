# Generated by Django 3.0.8 on 2021-01-06 08:18

import apps.project.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_auto_20210106_1526'),
        ('project', '0002_update_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='컨설턴트이름')),
                ('year', models.CharField(max_length=256, verbose_name='컨설턴트 경력년수')),
                ('content', models.CharField(max_length=256, verbose_name='컨설턴트 이력상세')),
                ('phoneNumber', models.CharField(max_length=256, verbose_name='컨설턴트 전화번호')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='세부일정')),
                ('startPeriod', models.IntegerField(verbose_name='시작일자')),
                ('endPeriod', models.IntegerField(verbose_name='종료일자')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Client', verbose_name='작성클라이언트'),
        ),
        migrations.AddField(
            model_name='project',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록일자'),
        ),
        migrations.AddField(
            model_name='project',
            name='estimate',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='견적'),
        ),
        migrations.AddField(
            model_name='project',
            name='explain',
            field=models.TextField(blank=True, null=True, verbose_name='설명'),
        ),
        migrations.AddField(
            model_name='project',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=apps.project.models.request_update_filename, verbose_name='의뢰파일'),
        ),
        migrations.AddField(
            model_name='project',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='연결된파트너'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('미정', '미정'), ('드랍', '드랍'), ('진행중', '진행중'), ('전환', '전환')], default='미정', max_length=10, null=True, verbose_name='진행현황'),
        ),
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='프로젝트 제목'),
        ),
        migrations.AddField(
            model_name='project',
            name='transferMoney',
            field=models.CharField(choices=[('아니오', '아니오'), ('선금입금', '선금입금'), ('완납', '완납')], default='아니오', max_length=10, verbose_name='입금 여부'),
        ),
        migrations.AlterField(
            model_name='request',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록일자'),
        ),
        migrations.CreateModel(
            name='ProposalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=256, verbose_name='가격정보')),
                ('period', models.CharField(max_length=256, verbose_name='기간정보')),
                ('task', models.ManyToManyField(to='project.Task', verbose_name='타입별세부일정')),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록일자')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Consultant', verbose_name='컨설턴트')),
                ('proposalType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.ProposalType', verbose_name='견적서타입')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fieldName', models.TextField(verbose_name='댓글 내용')),
                ('createAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록일자')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Client', verbose_name='작성클라이언트')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Comment', verbose_name='상위댓글')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='댓글이달린프로젝트')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='milestone',
            field=models.ManyToManyField(to='project.Task', verbose_name='주차별세부일정'),
        ),
        migrations.AddField(
            model_name='project',
            name='proposal',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Proposal', verbose_name='견적서'),
        ),
    ]
