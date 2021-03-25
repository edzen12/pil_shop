from django.db import models
from django.contrib.auth.models import User
from apps.products.models import ProductItem


class CartManager(models.Manager):

    def get_or_new(self, request):
        user = request.user
        cart_id = request.session.get('cart_id', None)
        if user is not None and user.is_authenticated:
            if user.cart:
                cart_obj = request.user.cart
            else:
                cart_obj = Cart.objects.get(pk=cart_id)
                cart_obj.user = user
                cart_obj.save()
            return cart_obj
        else:
            cart_obj = Cart.objects.get_or_create(pk=cart_id)
            cart_id = request.session['cart_id'] = cart_obj[0].id
            return cart_obj[0]


class Cart(models.Model):
    user = models.OneToOneField(User, verbose_name="Корзина", null=True, blank=True, on_delete=models.CASCADE)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = "Корзина"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина", related_name='cart_items')
    product_item = models.ForeignKey(ProductItem,  verbose_name="Позиция продукта",  related_name='product_in_cart', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1, verbose_name="количество", blank=True)

    def __str__(self):
        return f"{self.cart.id} = cart items"

    class Meta:
        verbose_name_plural = "Товары в Корзине"