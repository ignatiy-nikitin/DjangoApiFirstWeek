from rest_framework import serializers

from carts.models import Cart, CartItem
from items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
