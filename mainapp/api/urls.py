from django.urls import path
from .api_views import CategoryListApi, NotebookListApi, NotebookDetail, SmartphoneListApi, SmartphoneDetail

urlpatterns = [
    path('categories/', CategoryListApi.as_view(), name = 'categories_api'),
    path('notebooks/', NotebookListApi.as_view(), name = 'notebooks_api'),
    path('notebooks/<str:pk>/', NotebookDetail.as_view(), name = 'notebooks_detail'),
    path('smartphones/', SmartphoneListApi.as_view(), name = 'smartphones_api'),
    path('smartphones/<str:name>/', SmartphoneDetail.as_view(), name = 'smartphones_detail'),
]
