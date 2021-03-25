from django.db import models
from django.urls import reverse
from apps.categories.models import Category


PRODUCT_COLORS = (
    ('BLACK', 'Black'),
    ('BLUE', 'Blue'),
    ('RED', 'Red'),
    ('BROWN', 'Brown'),
    ('PURPLE', 'Purple'),
)


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='наименование товара')
    description = models.TextField( verbose_name='описание')
    categories = models.ManyToManyField(Category, verbose_name='категории', related_name='products')

    def __str__(self):
        return f"{self.name} - {self.categories}"
    
    class Meta:
        verbose_name_plural = "Продукты"

    def get_absolute_url(self):
        return reverse('product-detail', kwargs = {"pk" : self.pk})


class InStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(quantity=0)
    
    class Meta:
        verbose_name_plural = "На складе"


class ProductItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    class Meta:
        verbose_name_plural = "Менеджер по товарным позициям"


class ProductItem(models.Model):
    color = models.CharField(choices=PRODUCT_COLORS, verbose_name='цвет', max_length=255, db_index=True)
    size = models.CharField(verbose_name='размер', max_length=20)
    quantity = models.PositiveIntegerField(verbose_name='количество')
    price = models.DecimalField(max_digits=10, verbose_name='цена', decimal_places=2) # 2000.00
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт', related_name='product_items')

    objects = ProductItemManager()
    instock = InStockManager()

    def __str__(self):
        return f"{self.product.name}'s item of color {self.color}"

    def get_absolute_url(self):
        return reverse('productitem-detail', kwargs = {'pk' : self.pk})
    
    def add_to_bookmark_url(self):
        return reverse('add-to-bookmark', kwargs = {'pk': self.pk})
    
    class Meta:
        verbose_name_plural = "Позиция товара"
    



class ProductItemImage(models.Model):
    image = models.ImageField(upload_to='productImages', verbose_name='изображение')
    product_item = models.ForeignKey(ProductItem, verbose_name='Позиция товара', on_delete=models.CASCADE, related_name='product_item_images')

    def __str__(self):
        return f"{self.product_item.product.name}'s image of {self.product_item.color} item"

    class Meta:
        verbose_name_plural = "Изображение товара"