from django.template import Library
from django.utils.html import mark_safe
from mainapp.models import Product
from django.db.models import Count
register = Library()

@register.filter
def to_print(comment_list):
    res = """
    <ul style="list-style-type:none">
    <div class="col-md-12 mt-2">
    {}
    </div>
    </ul>
    """
    i = ''
    for comment in comment_list:
        i += """
        <li>
        {id}
        </li>
        <div class="col-md-12 mb-2 mt-2 p-0>
            <small>{user}</small>|опубликовано: {date_time}
            <hr>
            <div>{text}|id = {id}</div>
            <a href="#" class="reply" data-id="{id}" data-parent={parent_id}>Ответить</a>
            <form action="" method="POST" class="comment-form formm-group" id="form-{id}" style="display: none;">
                <textarea class="form-control" type="text" name="comment-text" ></textarea>
                <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="Отправить">
            </form>
        </div>
        """.format(id = comment['id'], user = comment['user'], date_time = comment['date_time'], parent_id = comment['parent_id'], text = comment['text'])
        if comment.get('children'):
            i += to_print(comment['children'])
    
    return mark_safe(res.format(i))



@register.simple_tag
def count_product(i):
    c=Product.objects.filter(category=i).count()
    return c
