# Generated by Django 3.1.4 on 2021-03-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20210301_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_prod',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=7, verbose_name='количество товаров'),
        ),
    ]