from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
import string
from django.http import request

from django.forms.widgets import Widget
from .models import Comment, Order, Product
from mainapp import models
from django.contrib.auth.models import User

class ZakazForm(forms.ModelForm):
    # created = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    # def __init__(self, *args, **kwargs):
    #     super().__init__( *args, **kwargs)
    #     self.fields['created'].label = 'Дата доставки'
    
    class Meta:
        model = Order
        fields = ('name', 'surname', 'adress', 'phone', 'delivery', 'comment')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username = username).exists():
            raise forms.ValidationError(f'Пользователь {username} не найден')
        user = User.objects.filter(username = username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Пароль неверный')
        return self.cleaned_data
    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'password','confirm_password', 'email', 'phone']

    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'email'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Телефон'
        self.fields['last_name'].label = 'Фамилия'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой почтой уже существует')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == confirm_password:
            if len(password) < 5:
                raise ValidationError('Пароль должен содержать не менее 5 символов')
        else:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        
class DispatchForm(forms.ModelForm):
    try:
        email = request.user.email
    except:
        email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Product
        fields = [
            'to', 'comments'
        ]




