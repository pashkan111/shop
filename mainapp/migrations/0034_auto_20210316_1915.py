# Generated by Django 3.1.4 on 2021-03-16 16:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0033_auto_20210316_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='will_be_delivered',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 20, 19, 15, 23, 793961), null=True, verbose_name='Будет доставлено'),
        ),
    ]
