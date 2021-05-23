from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from .models import Cart, Category, Comment, Customer, Cartproduct, Product
from django.shortcuts import redirect, render
from .forms import ZakazForm, LoginForm, RegistrationForm, CommentForm

class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user = request.user).first()
            if not customer:
                customer = Customer.objects.create(user = request.user)
            cart = Cart.objects.filter(owner = customer).first()
            if not cart:
                cart = Cart.objects.create(owner = customer)
        else:
            cart = Cart.objects.filter(for_anon = False)
            if not cart:
                cart = Cart.objects.create(for_anon = False)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_count(self, *args):
        cartprod_count = Cartproduct.objects.all().count()
        return cartprod_count

