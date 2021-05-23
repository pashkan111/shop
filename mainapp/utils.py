from django.db import models

def save_cart(cart):
    cart_data = cart.cartprod.aggregate(models.Sum('finalprice'), models.Count('id'))
    if cart_data.get('finalprice__sum'):
        cart.finalprice = cart_data.get('finalprice__sum')
    else:
        cart.finalprice__sum = 0
    cart.total_prod = cart_data.get('id__count')
    cart.save()

