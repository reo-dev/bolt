# Generated by Django 2.1.1 on 2020-04-14 02:29

import apps.category.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=256, verbose_name='제품중분류')),
                ('middle_img', models.ImageField(upload_to=apps.category.models.category_update_filename, verbose_name='중분류이미지')),
            ],
            options={
                'verbose_name': '  제품중분류',
                'verbose_name_plural': '  제품중분류',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=256, verbose_name='시/도')),
            ],
            options={
                'verbose_name': '시/도',
                'verbose_name_plural': '시/도',
            },
        ),
        migrations.CreateModel(
            name='Develop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=256, verbose_name='개발중분류')),
                ('coin', models.IntegerField(default=0, null=True, verbose_name='카테고리당 가격')),
            ],
            options={
                'verbose_name': '개발분야 중분류',
                'verbose_name_plural': '개발분야 중분류',
            },
        ),
        migrations.CreateModel(
            name='Developbig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maincategory', models.CharField(max_length=256, verbose_name='개발대분류')),
                ('maincategory_img', models.ImageField(null=True, upload_to=apps.category.models.developbig_update_filename, verbose_name='개발대분야 이미지')),
            ],
            options={
                'verbose_name': '개발분야 대분류',
                'verbose_name_plural': '개발분야 대분류',
            },
        ),
        migrations.CreateModel(
            name='Maincategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maincategory', models.CharField(max_length=256, verbose_name='제품대분류')),
                ('big_img', models.ImageField(upload_to=apps.category.models.maincategory_update_filename, verbose_name='제품대분류이미지')),
            ],
            options={
                'verbose_name': '  제품대분류',
                'verbose_name_plural': '  제품대분류',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=256, verbose_name='구')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.City', verbose_name='시/도')),
            ],
            options={
                'verbose_name': '구',
                'verbose_name_plural': '구',
            },
        ),
        migrations.CreateModel(
            name='Subclass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subclass', models.CharField(blank=True, max_length=256, verbose_name='제품소분류')),
                ('small_img', models.ImageField(upload_to=apps.category.models.subclass_update_filename, verbose_name='제품소분류이미지')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Category', verbose_name='제품중분류')),
                ('maincategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Maincategory', verbose_name='제품대분류')),
            ],
            options={
                'verbose_name': '  제품소분류',
                'verbose_name_plural': '  제품소분류',
            },
        ),
        migrations.AddField(
            model_name='develop',
            name='maincategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Developbig', verbose_name='개발대분류'),
        ),
        migrations.AddField(
            model_name='category',
            name='maincategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Maincategory', verbose_name='제품대분류'),
        ),
    ]
