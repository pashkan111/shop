# Generated by Django 3.1.4 on 2021-03-17 07:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0036_auto_20210316_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_child', to='mainapp.comment', verbose_name='Родитель'),
        ),
        migrations.AlterField(
            model_name='order',
            name='will_be_delivered',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 10, 31, 48, 633452), null=True, verbose_name='Будет доставлено'),
        ),
    ]