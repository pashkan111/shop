from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count
from django.db.transaction import commit

from django.contrib.contenttypes.fields import GenericForeignKey

from django.urls import reverse
User = get_user_model()

def get_models_for_count(*model_names):
    return list(models.Count(model_name) for model_name in model_names)


class CategoryManager(models.Manager):
    
    DICT = {
            'Ноутбук': 'notebook__count',
            'Смартфон': 'smartphone__count'
        }     
    def get_queryset(self):
        return super().get_queryset()

    def get_category(self):

        models = get_models_for_count('notebook', 'smartphone')
        qs = self.get_queryset().annotate(*models)
        data = [
            dict(name = c.name, slug = c.slug, count = getattr(c, self.DICT[c.name]), url = c.get_absolute_url()) for c in qs
            ]
        return data  




class LatestManager:

    @staticmethod
    def get_prod(*args):
        prod = []
        model = ContentType.objects.filter(model__in = args)
        for i in model:
            model_prod = i.model_class()._base_manager.all().order_by('-pk')
            prod.extend(model_prod)
        return prod

class Show:
    objects = LatestManager()





class Product(models.Model):
    
    name = models.CharField(verbose_name='название товара', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)
    price = models.DecimalField(max_digits=9, verbose_name='цена', decimal_places=0)
    description = models.TextField(verbose_name='описание')
    photo = models.ImageField(upload_to = 'products')
    category = models.ForeignKey('Category', verbose_name='категория', on_delete=models.CASCADE)
    # comment = models.ManyToManyField('Comment', blank=True)
    
    class Meta:
        abstract = True

def get_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    slug = obj.slug
    return reverse(viewname, args=[ct_model, slug])

        



class Category(models.Model):
    name = models.CharField(verbose_name='категория', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


# class Comment(models.Model):
#     text = models.TextField(verbose_name='Комментарий', max_length=500)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cartproduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='корзина', on_delete=models.CASCADE, related_name='related_cartproduct')
    quality = models.PositiveBigIntegerField(default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    finalprice = models.DecimalField(max_digits=9, verbose_name='финальная цена', decimal_places=0, default=0)

    def __str__(self):
        return 'Для корзины: {}'.format(self.content_object.name)

    def save(self, *args, **kwargs):
        self.finalprice = self.quality * self.content_object.price
        super().save(*args, **kwargs)

    def get_ct_model(self):
        ct_model = self.content_object._meta.model_name
        return ct_model
     

class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='владелец', on_delete=models.CASCADE, null=True)
    cartprod = models.ManyToManyField(Cartproduct, blank=True, related_name='related_cart')
    finalprice = models.DecimalField(verbose_name='цена всего', max_digits=9, decimal_places=0, default=0)
    in_order = models.BooleanField(default=True)
    for_anon = models.BooleanField(default=True)
    total_prod = models.DecimalField(verbose_name='количество товаров', max_digits=7, decimal_places=0, default=0)
   
    def __str__(self):
        return 'Cart № {}, of {}'.format(self.id, self.owner.user.username) 



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', null=True)
    phone = models.CharField(max_length=12, verbose_name='телефон')
    order = models.ManyToManyField('Order', related_name='customer_order')
    
    def __str__(self):
        return self.user.username



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
    created = models.DateTimeField(max_length=100, verbose_name='Время создания')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices = ORDER_STATUS,
        default=STATUS_NEW

    )

    delivery = models.CharField(
        max_length=100,
        verbose_name='',
        choices = TYPE_CHOISES,
        default = BY_YOURSELF
    )
    comment = models.TextField(max_length=500, verbose_name='Комментарий к заказу', blank=True, null=True)

    def __str__(self):
        return 'Order № {} of customer: {}'.format(self.id, self.customer.user.username)




class Notebook(Product):

    diagonal = models.DecimalField(verbose_name='диагональ', decimal_places=1, max_digits=10)
    processor = models.CharField(verbose_name='процессор', max_length=200)
    ram = models.DecimalField(verbose_name='оператива', decimal_places=1, max_digits=10)


    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return get_url(self, 'detail')



class Smartphone(Product):
    diagonal = models.DecimalField(verbose_name='диагональ', decimal_places=1, max_digits=10)
    color = models.CharField(verbose_name='цвет', max_length=200)
    camera = models.DecimalField(verbose_name='камера', decimal_places=1, max_digits=10)

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return get_url(self, 'detail')

