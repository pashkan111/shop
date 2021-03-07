from django import template
from django.utils.safestring import mark_safe


register = template.Library()


VALUES = """
        
            <p>{name}<p/>
            <p>{value}<p/>
        
"""
        # <tr>
        #     <td>{name}<td/>
        #     <td>{value}<td/>
        # <tr/>

TABLE_VALUES ={
    'notebook': {
       'Диагональ дисплея': 'diagonal',
       'Частота процессора': 'processor',
       'Оператива': 'ram'
    },
    'smartphone': {
        'Диагональ дисплея': 'diagonal',
        'Камера': 'camera',
        'Цвет': 'color',
    }
}




def get_product(product, model_name):
    res = ''
    for name, value in TABLE_VALUES[model_name].items():
        res += VALUES.format(name = name, value = getattr(product, value))
    return res

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(get_product(product, model_name))