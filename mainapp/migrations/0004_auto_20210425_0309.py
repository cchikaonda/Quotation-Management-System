# Generated by Django 3.0.9 on 2021-04-25 03:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210424_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]