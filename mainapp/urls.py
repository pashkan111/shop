
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import ShowDetail, CategoryDetail,  HomePage, CartPage, AddProdToCart, del_from_cart, ChangeQUALITY, Zakaz, GetForm, LoginView, Register, Profile, share_prod


urlpatterns = [
    path('home/', HomePage.as_view(), name = 'home'),
    # path('home/', home, name = 'home'),
    path('detail/<str:slug>', ShowDetail.as_view(), name = 'detail'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name = 'category_detail'),
    path('cart/', CartPage.as_view(), name = 'cart'),
    path('add_prod_to_cart/<str:slug>', AddProdToCart.as_view(), name = 'add_prod_to_cart'),
    # path('del_product_from_cart/<str:ct_model>/<str:slug>', DeleteFromCart.as_view(), name = 'del_product_from_cart'),
    path('del_product_from_cart/<str:slug>', del_from_cart, name = 'del_product_from_cart'),
    path('change_quality/<str:slug>', ChangeQUALITY.as_view(), name = 'change_quality'),
    path('zakaz/', Zakaz.as_view(), name = 'zakaz'),
    path('', GetForm.as_view(), name = 'delivery'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('register/', Register.as_view(), name = 'register'),
    path('logout/', LogoutView.as_view(next_page='/home/'), name = 'logout'),
    path('profile/', Profile.as_view(), name = 'profile'),
    path('share/<int:id>', share_prod, name = 'share'),
    
]