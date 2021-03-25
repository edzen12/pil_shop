from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',]
    save_on_top = True
    
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductItem)
admin.site.register(ProductItemImage)
