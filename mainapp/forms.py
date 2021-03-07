from django import forms
from django.forms import fields
from .models import Order

class ZakazForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields['created'].label = 'Дата доставки'


    created = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Order
        fields = ('name', 'surname', 'adress', 'phone', 'delivery', 'created', 'comment')