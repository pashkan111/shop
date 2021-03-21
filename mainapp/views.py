from django import forms
from django.db.models import base
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from .models import *
from .mixins import *
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import ZakazForm, LoginForm, RegistrationForm, CommentForm, DispatchForm
from .utils import *
from django.core.mail import send_mail 


class HomePage(CartMixin, ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self):
        context = super().get_context_data()
        context['category'] = Category.objects.all()
        context['cart'] = self.cart
        context['count'] = self.get_count()
        return context

class CartPage(CartMixin, View):
    def get(self, request, **kwargs):
        category = Category.objects.all()
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
        prod_slug = kwargs.get('slug')
        product = Product.objects.get(slug = prod_slug)
        cartprod, created = Cartproduct.objects.get_or_create(
            user = self.cart.owner, cart = self.cart, product = product
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
    prod_slug = kwargs.get('slug')
    product = Product.objects.get(slug = prod_slug)
    cartprod = Cartproduct.objects.get(
        user = cart.owner, cart = cart, product = product
    )  
    cart.cartprod.remove(cartprod)
    cartprod.delete()
    save_cart(cart)
    return HttpResponseRedirect('/cart/')


class ChangeQUALITY(CartMixin, View):
    def post(self, request, *args, **kwargs):
        prod_slug = kwargs.get('slug')
        
        product = Product.objects.get(slug = prod_slug)
        cartprod = Cartproduct.objects.get(
            user = self.cart.owner, cart = self.cart, product=product
        )       
        quality = request.POST.get('quality')
        cartprod.quality = int(quality)
        cartprod.save()
        save_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ShowDetail(CartMixin, CategoryDetailMixin, DetailView):
    
    template_name = 'detail.html'
    context_object_name = 'detail'
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_count()
        comment = Product.objects.first().comment.all()
        result = create_comment(comment)
        context['comment'] = result
        context['res'] = result
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.text = comment_form.cleaned_data['text']
            new_comment.content_type = ContentType.objects.get(model='product')
            new_comment.object_id = 1
            new_comment.parent = None
            new_comment.is_child = False
            new_comment.save()
            return HttpResponseRedirect('')
        return super().dispatch(request, *args, **kwargs)
    # def get_queryset(self):
    #     comment = Product.objects.first().comment.all()
    #     result = create_comment(comment)
    #     print(result)

    # def get(self, request, *args, **kwargs):
    #     comment_form = CommentForm(request.POST or None)
    #     context = {
    #         'comment_form': comment_form
    #     }
    #     return render(request, 'detail.html', context=context)


def get_comment(request):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='product')
        new_comment.object_id = 1
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return HttpResponseRedirect('')




class CategoryDetail(CategoryDetailMixin, ListView):
    
    template_name = 'category_detail.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        products  = Product.objects.filter(category = category)
        return products
    
    def get_context_data(self, **kwargs):
        context = {'prod': self.get_queryset()}
        context['category'] = Category.objects.all()
        return context

class LoginView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        category = Category.objects.all()
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/home/')
        return self.get()

class Register(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        category = Category.objects.all()
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.phone = form.cleaned_data['phone']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user = new_user,
                phone = new_user.phone
            )
            user=authenticate(username = new_user.username, password = form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/home/')
        return self.get(request)

class Profile(CartMixin, View):
    def get(self, request, *args):
        customer = Customer.objects.get(user = request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(customer=customer)
        context = {
            'orders': orders,
            'cat': categories,
            'cart': self.cart
        }
        return render(request, 'profile.html', context=context)
        



# class GetDispatch(View):
#     def get(self, request, *args, **kwargs):
#         form = Dispatch(request.POST or None)
#         context = {
#             'form': form
#         }
#         return render(request, 'dispatch.html', context)
def share_prod(request, **kwargs):
    prod = get_object_or_404(Product, id=kwargs['id'])
    sent = False
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(prod.get_absolute_url())
            subject = '{} recommends you reading {}'.format( cd['email'], prod.name)
            message = 'Read {} {} comments:{}'.format(prod.name, post_url, cd['comments'])
            send_mail(subject, message, 'kozhevnikov0001@yandex.ru', [cd['to']])
            sent = True
            return HttpResponseRedirect('/home/')
    else:
        form = DispatchForm(request.POST) 
        return render(request, 'dispatch.html', {'form': form})
 