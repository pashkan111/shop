from django.urls import path
from .views import ShowFeatures


urlpatterns = [
    path('featuresadmin/', ShowFeatures.as_view(), name = 'featuresadmin'),
]