from django.contrib import admin
from .models import *


class ProductItemImageInline(admin.TabularInline):
    model = ProductItemImage
    extra = 1

admin.site.register(ProductItemImage)

class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductItemImageInline,]
    save_on_top = True
    
admin.site.register(ProductItem, ProductItemAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',]
    save_on_top = True
    
admin.site.register(Product, ProductAdmin)


