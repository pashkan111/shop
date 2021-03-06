# Generated by Django 3.1.4 on 2021-03-04 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_cart_total_prod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('adress', models.CharField(max_length=100, verbose_name='Адрес')),
                ('created', models.DateTimeField(max_length=100, verbose_name='Время создания')),
                ('phone', models.CharField(max_length=100, verbose_name='Телефон')),
                ('status', models.CharField(choices=[('STATUS_NEW', 'Новый заказ'), ('STATUS_IN_PROGRESS', 'Заказ в пути'), ('STATUS_READY', 'Заказ готов к получению'), ('STATUS_DELIVERED', 'Заказ доставлен')], default='new', max_length=100, verbose_name='')),
                ('delivery', models.CharField(choices=[('BY_YOURSELF', 'Самовывоз'), ('DELIVERY', 'Доставка курьером')], default='by_yourself', max_length=100, verbose_name='')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_customer', to='mainapp.customer', verbose_name='Покупатель')),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AddField(
            model_name='customer',
            name='order',
            field=models.ManyToManyField(related_name='customer_order', to='mainapp.Order'),
        ),
    ]
