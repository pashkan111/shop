# Generated by Django 3.1.4 on 2021-03-08 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_auto_20210307_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='comment',
        ),
    ]