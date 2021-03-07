
from django.urls import path
from .views import ShowDetail, CategoryDetail,  HomePage, CartPage, AddProdToCart, del_from_cart, ChangeQUALITY, Zakaz, GetForm


urlpatterns = [
    path('home/', HomePage.as_view(), name = 'home'),
    # path('home/', home, name = 'home'),
    path('detail/<str:ct_model>/<str:slug>', ShowDetail.as_view(), name = 'detail'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name = 'category_detail'),
    path('cart/', CartPage.as_view(), name = 'cart'),
    path('add_prod_to_cart/<str:ct_model>/<str:slug>', AddProdToCart.as_view(), name = 'add_prod_to_cart'),
    # path('del_product_from_cart/<str:ct_model>/<str:slug>', DeleteFromCart.as_view(), name = 'del_product_from_cart'),
    path('del_product_from_cart/<str:ct_model>/<str:slug>', del_from_cart, name = 'del_product_from_cart'),
    path('change_quality/<str:ct_model>/<str:slug>', ChangeQUALITY.as_view(), name = 'change_quality'),
    path('zakaz/', Zakaz.as_view(), name = 'zakaz'),
    path('', GetForm.as_view(), name = 'delivery'),
]