from django.contrib.contenttypes import fields
from rest_framework import serializers
from ..models import Category, Notebook, Smartphone


class CategorySerial(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]

class BaseProductSerial:
    name = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    price = serializers.DecimalField(required=True, max_digits = 9, decimal_places = 0)
    description = serializers.CharField(required=False)
    photo = serializers.ImageField(required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)


class NotebookSerial(BaseProductSerial, serializers.ModelSerializer):
    diagonal = serializers.DecimalField(required=True, max_digits = 9, decimal_places = 1)
    processor = serializers.CharField(required=True)
    ram = serializers.DecimalField(required=True, max_digits = 3, decimal_places = 0)

    class Meta:
        model = Notebook
        fields = '__all__'


class SmartphoneSerial(BaseProductSerial, serializers.ModelSerializer):
    diagonal = serializers.DecimalField(required=True, decimal_places=1, max_digits=10)
    color = serializers.CharField(required=True)
    camera = serializers.DecimalField(required=True, decimal_places=1, max_digits=10)

    class Meta:
        model = Smartphone
        fields = '__all__'