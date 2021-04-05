from django.db import models

class CategoryFeatures(models.Model):
    category = models.ForeignKey(
        "mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE
        )
    feature_name = models.CharField(max_length=100, verbose_name='Имя характеристики')
    measure = models.CharField(max_length=20, verbose_name='Единица измерения')

    class Meta():
        unique_together = ('category', 'feature_name')

    def __str__(self) -> str:
        return f'Для категории: {self.category.name} характеристика: {self.feature_name}'

class FeaturesValid(models.Model):
    category = models.ForeignKey(
        "mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE
        )
    feature_key = models.ForeignKey(
        CategoryFeatures, on_delete=models.CASCADE, verbose_name='Ключ характеристики'
        )
    valid_feature_value = models.CharField(max_length=100, verbose_name='Валидное значение')
    
    def __str__(self) -> str:
        return f'Категория: {self.category.name} наименование характеристики: {self.feature_key.feature_name} валидное значение: {self.valid_feature_value}'

class ProductFeatures(models.Model):

    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE, verbose_name='Товар')
    feature = models.ForeignKey(CategoryFeatures, on_delete=models.CASCADE, verbose_name='Характеристика товара')
    value = models.CharField(verbose_name='Значение', max_length=100)

    def __str__(self) -> str:
        return f'Продукт: {self.product.name} характеристика: {self.feature} значение: {self.value}'
