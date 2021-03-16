from django.contrib.contenttypes import fields
from rest_framework import serializers
from ..models import Category


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


