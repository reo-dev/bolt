# Generated by Django 3.0.8 on 2021-02-15 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shopcategory', '0001_initial'),
        ('shopaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=256, verbose_name='구매옵션')),
                ('request', models.TextField()),
                ('orderDate', models.DateTimeField()),
                ('status', models.CharField(max_length=256, verbose_name='주문상태')),
            ],
            options={
                'verbose_name': '     주문',
                'verbose_name_plural': '     주문',
            },
        ),
        migrations.CreateModel(
            name='RegularOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nextPayment', models.DateTimeField(verbose_name='다음 결제일')),
                ('paymentPeriod', models.CharField(max_length=256, verbose_name='결제주기')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
            ],
            options={
                'verbose_name': 'Regular',
                'verbose_name_plural': 'Regulars',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('thumbnailImage', models.ImageField(upload_to=None)),
                ('mainImage', models.ImageField(upload_to=None)),
                ('explain', models.TextField()),
                ('stockQuantity', models.IntegerField(verbose_name='재고수량')),
                ('bigCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopcategory.BigCategory')),
                ('middleCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopcategory.MiddleCategory')),
                ('smallCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopcategory.SmallCategory')),
            ],
            options={
                'verbose_name': '     상품',
                'verbose_name_plural': '     상품',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('orderPrice', models.CharField(max_length=256, verbose_name='주문가격')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
            options={
                'verbose_name': '     주문상품',
                'verbose_name_plural': '     주문상품',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='OrderProduct',
            field=models.ManyToManyField(related_name='orders', through='shop.OrderProduct', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopaccount.ShopClient'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopaccount.ShopClient')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
    ]
