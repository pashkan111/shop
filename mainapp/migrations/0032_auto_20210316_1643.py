# Generated by Django 3.1.4 on 2021-03-16 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0031_auto_20210316_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='will_be_delivered',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 20, 16, 43, 22, 760335), null=True, verbose_name='Будет доставлено'),
        ),
    ]
