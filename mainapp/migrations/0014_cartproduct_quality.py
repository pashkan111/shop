# Generated by Django 3.1.4 on 2021-02-28 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20210225_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='quality',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]