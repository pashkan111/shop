from django.urls import path
from .views import MainMenu, NewCategoryView, NewFeature, ValueFeatureProduct


urlpatterns = [
    path('', MainMenu.as_view(), name = 'main_menu'),
    path('add_category/', NewCategoryView.as_view(), name = 'add_category'),
    path('add_feature/', NewFeature.as_view(), name = 'add_feature'),
    path('product_value/', ValueFeatureProduct.as_view(), name = 'product_value'),
]