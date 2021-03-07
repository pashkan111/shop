from django.contrib import admin

from .models import*
from django.forms import ModelForm, ValidationError
from PIL import Image

# class NotebookForm(ModelForm):

#     MIN_IMAGE = (400, 400)
#     MAX_IMAGE = (1000, 1000)

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         self.fields['photo'].help_text = 'Изображение должно быть минимум {}x{}'.format(*self.MIN_IMAGE)
    
#     def clean_photo(self):
#         photo = self.cleaned_data['photo']
#         photo = Image.open(photo)
       
#         min_height, min_width = self.MIN_IMAGE
#         max_height, max_width = self.MAX_IMAGE
#         if photo.height<min_height or photo.width<min_width:
#             raise ValidationError('Фотка не соответствует параметрам')
#         if photo.height>max_height or photo.width>max_width:
#             raise ValidationError('Фотка не соответствует параметрам')
        


class NotebookAdmin(admin.ModelAdmin):
    # form = NotebookForm
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'diagonal', 'processor')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class SmartphoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Cartproduct)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Customer)
admin.site.register(Order)


