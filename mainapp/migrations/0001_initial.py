# Generated by Django 3.0.9 on 2021-04-14 19:45

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'General User')], default='General User', max_length=15)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('superuser', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='avatar0.jpg', null=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('address', models.CharField(max_length=120)),
                ('phone_number', models.CharField(max_length=15)),
                ('country', models.CharField(default='MALAWI', max_length=50)),
                ('total_quotations', models.IntegerField(default=0)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.CharField(max_length=100)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='MWK', max_digits=14)),
                ('discount_price_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('discount_price', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MWK', max_digits=14, null=True)),
                ('active', models.BooleanField(default=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('category_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_short_name', models.CharField(max_length=10)),
                ('unit_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('ordered_item_price_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('ordered_item_price', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('ordered_items_total_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('ordered_items_total', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_item', to='mainapp.Item')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateField(null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending ...'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending ...', max_length=15)),
                ('markup', models.FloatField(choices=[(38.0, 'Markup A'), (35.0, 'Markup B'), (30.0, 'Markup C')], default=38.0)),
                ('markup_value_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('markup_value', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('labour_p', models.FloatField(default=15.0)),
                ('labour_cost_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('labour_cost', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('order_total_cost_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('order_total_cost', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('vat_p', models.FloatField(default=10.5)),
                ('vat_cost_currency', djmoney.models.fields.CurrencyField(choices=[('MWK', 'Malawian Kwacha')], default='MWK', editable=False, max_length=3)),
                ('vat_cost', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='MWK', max_digits=14)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Customer')),
                ('items', models.ManyToManyField(to='mainapp.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ItemCategory'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Unit'),
        ),
    ]
