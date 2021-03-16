from django.http import request
from django.shortcuts import render
from django.views import View




class ShowFeatures(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'product_features.html', {})
