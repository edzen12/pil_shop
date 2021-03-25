from rest_framework import serializers

from apps.products.serializers import ProductItemSerializer
from .models import Cart, CartItem


class CartSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items',)


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('amount', 'product_item')
