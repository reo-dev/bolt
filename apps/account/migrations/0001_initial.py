# Generated by Django 2.1.1 on 2020-04-14 02:29

import apps.account.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default=apps.account.models.get_default_hash_id, max_length=256, unique=True, verbose_name='이메일')),
                ('type', models.IntegerField(choices=[(0, 'CLIENT'), (1, 'PARTNER')], default=0, verbose_name='유저타입')),
                ('password', models.CharField(max_length=256)),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='휴대폰 번호')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '가입자',
                'verbose_name_plural': '가입자',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_certification', models.ImageField(null=True, upload_to=apps.account.models.certification_update_filename, verbose_name='보유인증서 이미지')),
                ('is_main', models.BooleanField(default=False, verbose_name='메인 여부')),
            ],
            options={
                'verbose_name': '     보유인증서',
                'verbose_name_plural': '     보유인증서',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'verbose_name': '클라이언트',
                'verbose_name_plural': '클라이언트',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_machine', models.ImageField(null=True, upload_to=apps.account.models.machine_update_filename, verbose_name='보유장비 이미지')),
                ('is_main', models.BooleanField(default=False, verbose_name='메인 여부')),
            ],
            options={
                'verbose_name': '     보유장비',
                'verbose_name_plural': '     보유장비',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True, verbose_name='업체명')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=apps.account.models.partner_update_filename, verbose_name='로고')),
                ('career', models.CharField(max_length=256, null=True, verbose_name='설립일')),
                ('employee', models.CharField(max_length=256, null=True, verbose_name='근로자수')),
                ('revenue', models.CharField(max_length=256, null=True, verbose_name='매출(백만원)')),
                ('info_company', models.TextField(blank=True, null=True, verbose_name='회사소개')),
                ('info_biz', models.TextField(blank=True, null=True, verbose_name='주요사업')),
                ('history', models.TextField(blank=True, null=True, verbose_name='주요이력')),
                ('deal', models.TextField(blank=True, null=True, verbose_name='주요거래처')),
                ('coin', models.IntegerField(default=0, null=True, verbose_name='코인')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.account.models.partner_update_filename, verbose_name='회사소개 및 포토폴리오파일')),
                ('avg_score', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True, verbose_name='평균점수')),
                ('category_middle', models.ManyToManyField(related_name='category_middle', to='category.Develop', verbose_name='의뢰가능분야')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.City', verbose_name='시/도')),
                ('history_set', models.ManyToManyField(related_name='history_product', to='category.Subclass', verbose_name='진행한제품들')),
                ('possible_set', models.ManyToManyField(related_name='possible_product', to='category.Subclass', verbose_name='개발가능제품분야')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Region', verbose_name='구')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'verbose_name': '파트너',
                'verbose_name_plural': '파트너',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_portfolio', models.ImageField(null=True, upload_to=apps.account.models.portfolio_update_filename, verbose_name='포토폴리오 이미지')),
                ('is_main', models.BooleanField(default=False, verbose_name='메인 여부')),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너')),
            ],
            options={
                'verbose_name': '     포트폴리오',
                'verbose_name_plural': '     포트폴리오',
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_process', models.ImageField(null=True, upload_to=apps.account.models.process_update_filename, verbose_name='진행공정 이미지')),
                ('is_main', models.BooleanField(default=False, verbose_name='메인 여부')),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너')),
            ],
            options={
                'verbose_name': '     진행공정',
                'verbose_name_plural': '     진행공정',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_structure', models.ImageField(null=True, upload_to=apps.account.models.structure_update_filename, verbose_name='조직도 이미지')),
                ('is_main', models.BooleanField(default=False, verbose_name='메인 여부')),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너')),
            ],
            options={
                'verbose_name': '     조직도',
                'verbose_name_plural': '     조직도',
            },
        ),
        migrations.AddField(
            model_name='machine',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너'),
        ),
        migrations.AddField(
            model_name='certification',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Partner', verbose_name='파트너'),
        ),
    ]
