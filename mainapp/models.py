from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count
from django.db.transaction import commit
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.fields import GenericRelation

from django.urls import reverse
User = get_user_model()


class Product(models.Model):
    
    name = models.CharField(verbose_name='название товара', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)
    price = models.DecimalField(max_digits=9, verbose_name='цена', decimal_places=0)
    description = models.TextField(verbose_name='описание')
    photo = models.ImageField(upload_to = 'products')
    category = models.ForeignKey('Category', verbose_name='категория', on_delete=models.CASCADE)
    comment = GenericRelation('comment')

    def __str__(self):
        return self.name
         
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True, 
        verbose_name='Родитель',
        on_delete=models.CASCADE,
        related_name='comment_child'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    time_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')
    is_child = models.BooleanField(default=False)

    @property
    def define_parent(self):
        if not self.parent:
            return ''
        return self.parent

class Category(models.Model):
    name = models.CharField(verbose_name='категория', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Cartproduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='корзина', on_delete=models.CASCADE, related_name='related_cartproduct')
    quality = models.PositiveBigIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    finalprice = models.DecimalField(max_digits=9, verbose_name='финальная цена', decimal_places=0, default=0)
 
    def __str__(self):
        return 'Для корзины: {}'.format(self.content_object.name)

    def save(self, *args, **kwargs):
        self.finalprice = self.quality * self.product.price
        super().save(*args, **kwargs)
     

class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='владелец', on_delete=models.CASCADE, null=True)
    cartprod = models.ManyToManyField(Cartproduct, blank=True, related_name='related_cart')
    finalprice = models.DecimalField(verbose_name='цена всего', max_digits=9, decimal_places=0, default=0)
    in_order = models.BooleanField(default=True)
    for_anon = models.BooleanField(default=True)
    total_prod = models.DecimalField(verbose_name='количество товаров', max_digits=7, decimal_places=0, default=0)
   
    def __str__(self):
        return 'Cart № {}'.format(self.id) 



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', null=True)
    phone = models.CharField(max_length=12, verbose_name='телефон')
    order = models.ManyToManyField('Order', related_name='customer_order')
    
    def __str__(self):
        return f'{self.user.username}, {self.id}'



class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_DELIVERED = 'is_delivered'
    BY_YOURSELF = 'by_yourself'
    DELIVERY = 'delivery'
    
    ORDER_STATUS = (
        ('STATUS_NEW', 'Новый заказ'),
        ('STATUS_IN_PROGRESS', 'Заказ в пути'),
        ('STATUS_READY', 'Заказ готов к получению'),
        ('STATUS_DELIVERED', 'Заказ доставлен')
    )
    TYPE_CHOISES = (
        ('BY_YOURSELF', 'Самовывоз'),
        ('DELIVERY', 'Доставка курьером')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE, related_name='order_customer')

    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    adress = models.CharField(max_length=100, verbose_name='Адрес')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    will_be_delivered = models.DateTimeField(verbose_name='Будет доставлено', default=datetime.datetime.now() + datetime.timedelta(days=4), null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices = ORDER_STATUS,
        default=STATUS_NEW

    )
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    delivery = models.CharField(
        max_length=100,
        verbose_name='',
        choices = TYPE_CHOISES,
        default = BY_YOURSELF
    )
    def __str__(self):
        return 'Order № {}'.format(self.id)




