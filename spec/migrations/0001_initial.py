# Generated by Django 3.1.4 on 2021-03-15 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0028_auto_20210315_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='Имя характеристики')),
                ('feature_filter_name', models.CharField(max_length=100, verbose_name='Имя фильтра')),
                ('measure', models.CharField(max_length=20, verbose_name='Единица измерения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'unique_together': {('category', 'feature_name', 'feature_filter_name')},
            },
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='Значение')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spec.categoryfeature', verbose_name='Характеристика товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_feature_value', models.CharField(max_length=100, verbose_name='Валидное значение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spec.categoryfeature', verbose_name='Ключ характеристики')),
            ],
        ),
    ]
