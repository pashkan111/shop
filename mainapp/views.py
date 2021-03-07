from django import forms
from django.db.models import base
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.http import request
from django.views.generic.base import View
from .models import *
from .mixins import *
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import ZakazForm
from .utils import save_cart



class HomePage(CartMixin, ListView):
    model = ContentType
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Show.objects.get_prod('notebook', 'smartphone')
        return products

    def get_context_data(self, **kwargs):
        context = {'products': self.get_queryset()}
        context['category'] = Category.objects.get_category()
        context['cart'] = self.cart
        context['count'] = self.get_count()
        return context

class CartPage(CartMixin, View):
    def get(self, request, **kwargs):
        category = Category.objects.get_category()
        save_cart(self.cart)
        context = {
            'cart': self.cart,
            'category': category,
            'count': self.get_count()
        }
        return render(request, 'cart.html', context = context)


class Zakaz(CartMixin, View):
    def get(self, request, **kwargs):
        form = ZakazForm(request.POST or None)
        context = {
            'cart': self.cart,
            'count': self.get_count(),
            'form': form
        }
        return render(request, 'zakaz.html', context = context)

class GetForm(CartMixin, View):
     
    def post(self, request, *args, **kwargs):
        form = ZakazForm(request.POST or None)
        customer = Customer.objects.get(user = request.user)
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.customer = customer
            order_form.name = form.cleaned_data['surname']
            order_form.adress = form.cleaned_data['adress']
            order_form.phone = form.cleaned_data['phone']
            order_form.delivery = form.cleaned_data['delivery']
            order_form.created = form.cleaned_data['created']
            order_form.comment = form.cleaned_data['comment']
            order_form.save()

            self.cart.save()
            order_form.cart = self.cart
            order_form.save()
            customer.order.add(order_form)
            print(form.cleaned_data)
            return HttpResponseRedirect('/home/')
        return HttpResponseRedirect('zakaz/')





class AddProdToCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = prod_slug)
        cartprod, created = Cartproduct.objects.get_or_create(
            user = self.cart.owner, cart = self.cart, content_type=content_type, object_id = product.id
        )       
        self.cart.cartprod.add(cartprod)
        save_cart(self.cart)
        return HttpResponseRedirect('/cart/')


# class DeleteFromCart(CartMixin,View):

#     def del_prod(self, **kwargs):
#         ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
#         content_type = ContentType.objects.get(model = ct_model)
#         product = content_type.model_class().objects.get(slug = prod_slug)
#         cartprod = Cartproduct.objects.get(
#             user = self.cart.owner, cart = self.cart, content_type=content_type, object_id = product.id
#         )  
#         self.cart.cartprod.remove(cartprod)
#         cartprod.delete()
#         self.cart.save() 
        
#         return HttpResponseRedirect('/cart/')


def del_from_cart(request, *args, **kwargs):          
            
    customer, created_customer = Customer.objects.get_or_create(user = request.user)
    cart, created_cart = Cart.objects.get_or_create(owner = customer)
    ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
    content_type = ContentType.objects.get(model = ct_model)
    product = content_type.model_class().objects.get(slug = prod_slug)
    cartprod = Cartproduct.objects.get(
        user = cart.owner, cart = cart, content_type=content_type, object_id = product.id
    )  
    cart.cartprod.remove(cartprod)
    cartprod.delete()
    save_cart(cart)
    return HttpResponseRedirect('/cart/')


class ChangeQUALITY(CartMixin, View):
    def post(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = prod_slug)
        cartprod = Cartproduct.objects.get(
            user = self.cart.owner, cart = self.cart, content_type=content_type, object_id = product.id
        )       
        quality = request.POST.get('quality')
        cartprod.quality = int(quality)
        cartprod.save()
        save_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ShowDetail(CartMixin, CategoryDetailMixin,DetailView):
    CT_MODEL = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    template_name = 'detail.html'
    context_object_name = 'detail'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['count'] = self.get_count()
        return context

class CategoryDetail(CategoryDetailMixin, ListView):
    CT_MODEL = {
    'noutbuk': 'notebook',
    'smartfon': 'smartphone',
}
    template_name = 'category_detail.html'

    def get_queryset(self):
        model = self.CT_MODEL[self.kwargs['slug']]
        products = Show.objects.get_prod(model)
        return products
    
    def get_context_data(self, **kwargs):
        context = {'prod': self.get_queryset()}
        context['category'] = Category.objects.get_category()
        return context