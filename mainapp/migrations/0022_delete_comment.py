# Generated by Django 3.1.4 on 2021-03-08 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_remove_product_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
