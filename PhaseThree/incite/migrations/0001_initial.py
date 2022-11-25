# Generated by Django 3.2.16 on 2022-11-25 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('Firstname', models.CharField(max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('CartID', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('CustomerID', models.AutoField(primary_key=True, serialize=False)),
                ('ship_addr', models.CharField(max_length=200)),
                ('bill_addr', models.CharField(max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('SellerID', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ProductID', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('stock', models.IntegerField()),
                ('sellerid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('OrderID', models.IntegerField(primary_key=True, serialize=False)),
                ('Order_Date', models.DateTimeField(auto_now_add=True)),
                ('Receipt_Date', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('OrderItemID', models.IntegerField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.orders')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.product')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('CheckoutID', models.IntegerField(primary_key=True, serialize=False)),
                ('CartID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.cart')),
                ('CustomerID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incite.customer')),
                ('SellerID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.seller')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='CustomerID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='OrderID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='incite.orders'),
        ),
    ]