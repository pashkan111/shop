from django.urls import path
from .api_views import CategoryListApi

urlpatterns = [
    path('categories/', CategoryListApi.as_view(), name = 'categories_api'),
]
