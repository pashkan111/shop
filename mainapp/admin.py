from django.contrib import admin
from .models import*

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Cartproduct)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)


