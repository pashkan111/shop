from django.db.transaction import commit
from django.http import request
from django.shortcuts import render
from django.views import View
from .forms import FeatureForm, FeatureCategoryForm, FeatureValue
from django.http import HttpResponseRedirect




class MainMenu(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'product_features.html', {})

class NewCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = FeatureForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'category_view.html', context)

    def post(self, request, *args, **kwargs):
        form = FeatureForm(request.POST or None)
        if form.is_valid():
            form.save()
        return render(request, 'product_features.html', {})


class NewFeature(View):

    def get(self, request, *args, **kwargs):
        form = FeatureCategoryForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'feature_view.html', context)

    def post(self, request, *args, **kwargs):
        form = FeatureCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
        return render(request, 'product_features.html', {})


class ValueFeatureProduct(View):
    def get(self, request, *args, **kwargs):
        form = FeatureValue(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'feature_view.html', context)

    def post(self, request, *args, **kwargs):
        form = FeatureCategoryForm(request.POST or None)
        if form.is_valid():
            new_value = form.save(commit=False)
            new_value.product = form.cleaned_data['product']
            new_value.value = form.cleaned_data['value']
            new_value.save()
        return render(request, 'product_value.html')

