from django import forms
from django.forms import fields
from mainapp.models import Category
from spec.models import *

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class FeatureCategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryFeatures
        fields = '__all__'

class FeatureValue(forms.ModelForm):
    class Meta:
        model = ProductFeatures
        fields = '__all__'