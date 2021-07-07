# Generated by Django 3.0.8 on 2021-04-13 07:43

import apps.project.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0054_auto_20210413_1634'),
        ('project', '0063_auto_20210218_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_parts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_width', models.IntegerField(blank=True, default=0, null=True, verbose_name='도면 가로')),
                ('product_depth', models.IntegerField(blank=True, default=0, null=True, verbose_name='도면 세로')),
                ('product_height', models.IntegerField(blank=True, default=0, null=True, verbose_name='도면 높이')),
                ('auto_price', models.CharField(blank=True, max_length=256, null=True, verbose_name='자동 견적 가격')),
                ('product_status', models.BooleanField(default=False, null=True, verbose_name='도면 유무')),
                ('product_type', models.CharField(blank=True, max_length=256, null=True, verbose_name='도면 형상 type')),
            ],
            options={
                'verbose_name': '     추가한 도면 정보',
                'verbose_name_plural': '     추가한 도면 정보',
            },
        ),
        migrations.RemoveField(
            model_name='answer',
            name='active',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='all_price',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='category',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='client',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='day',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='expert',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='file',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='info_check',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='open_time',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='people',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='period',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='price',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='send_meeting',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='state',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='strategy',
        ),
        migrations.RemoveField(
            model_name='project',
            name='client',
        ),
        migrations.RemoveField(
            model_name='project',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='project',
            name='develop',
        ),
        migrations.RemoveField(
            model_name='project',
            name='file',
        ),
        migrations.RemoveField(
            model_name='project',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='project',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='request',
            name='period',
        ),
        migrations.RemoveField(
            model_name='request',
            name='price',
        ),
        migrations.RemoveField(
            model_name='request',
            name='product',
        ),
        migrations.RemoveField(
            model_name='request',
            name='proposal',
        ),
        migrations.RemoveField(
            model_name='request',
            name='sendInformation',
        ),
        migrations.AddField(
            model_name='answer',
            name='check_time',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='제안서 최종 확인 시간'),
        ),
        migrations.AddField(
            model_name='answer',
            name='content1',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='컨텐츠1'),
        ),
        migrations.AddField(
            model_name='answer',
            name='content2',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='컨텐츠2'),
        ),
        migrations.AddField(
            model_name='answer',
            name='content3',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='컨텐츠3'),
        ),
        migrations.AddField(
            model_name='answer',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Request', verbose_name='의뢰서 모델'),
        ),
        migrations.AddField(
            model_name='request',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='납기일'),
        ),
        migrations.AddField(
            model_name='request',
            name='order_request_close',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='비공개 발주 요청사항'),
        ),
        migrations.AddField(
            model_name='request',
            name='order_request_open',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='공개 발주 요청사항'),
        ),
        migrations.AddField(
            model_name='request',
            name='product_inform',
            field=models.FileField(blank=True, max_length=256, null=True, upload_to=apps.project.models.request_update_filename, verbose_name='도면 정보'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너'),
        ),
        migrations.CreateModel(
            name='Reuqest_parts_list',
            fields=[
                ('product_img', models.ImageField(null=True, upload_to=apps.project.models.request_update_filename, verbose_name='도면 형상 이미지')),
                ('price', models.CharField(max_length=256, null=True, verbose_name='가격정보')),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='project.Request_parts', verbose_name='도면 정보')),
            ],
            options={
                'verbose_name': '     선택한 도면 정보',
                'verbose_name_plural': '     선택한 도면 정보',
            },
        ),
        migrations.AddField(
            model_name='request_parts',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.Request', verbose_name='의뢰서'),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_content', models.TextField(null=True, verbose_name='채팅 내용')),
                ('user_type', models.IntegerField(blank=True, choices=[(0, '클라이언트'), (1, '파트너')], default=0, null=True, verbose_name='글쓴이 타입')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='작성일자')),
                ('chat_type', models.CharField(choices=[(0, '텍스트'), (1, '이미지'), (2, '파일')], max_length=256, null=True, verbose_name='채팅 타입')),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Answer', verbose_name='제안서')),
            ],
            options={
                'verbose_name': '채팅',
                'verbose_name_plural': '채팅',
            },
        ),
    ]
