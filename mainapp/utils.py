from django.db import models
from .models import Comment, Product

def save_cart(cart):
    cart_data = cart.cartprod.aggregate(models.Sum('finalprice'), models.Count('id'))
    if cart_data.get('finalprice__sum'):
        cart.finalprice = cart_data.get('finalprice__sum')
    else:
        cart.finalprice__sum = 0
    cart.total_prod = cart_data.get('id__count')
    cart.save()



def define_child(qs_child):
    result=[]
    for comment in qs_child:
        res = {
        'id': comment.id,
        'text': comment.text,
        'user': comment.user,
        'parent_id': comment.define_parent,
        'date_time': comment.time_date,
        'is_child': comment.is_child,
        }
        if comment.comment_child.exists():
            res['children'] = define_child(comment.comment_child.all())
        result.append(res)
    return result


def create_comment(qs):
    result=[]
    for comment in qs:
        res = {
        'id': comment.id,
        'text': comment.text,
        'user': comment.user,
        'parent_id': comment.define_parent,
        'date_time': comment.time_date,
        'is_child': comment.is_child,
        }
        if comment.comment_child:
            res['children'] = define_child(comment.comment_child.all())
        if not comment.is_child:
            result.append(res)
    return result
