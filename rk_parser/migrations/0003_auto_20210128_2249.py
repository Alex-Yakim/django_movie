# Generated by Django 3.1.4 on 2021-01-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rk_parser', '0002_product_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(max_length=100, unique=True, verbose_name='Артикул'),
        ),
    ]
