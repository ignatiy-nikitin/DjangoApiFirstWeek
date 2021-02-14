from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from carts.models import Cart, CartItem
from items.models import Item
from items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'price', 'total_price']
        extra_kwargs = {
            'item_id': {'required': True},
            'quantity': {'required': True},
        }

    def create(self, validated_data):
        print(validated_data)
        cart_item, _ = CartItem.objects.update_or_create(
            cart=self.context['request'].user.cart,
            item=validated_data['item'],
            defaults={
                'quantity': validated_data['quantity'],
                'price': validated_data['item'].price,
            }
        )
        return cart_item

    def update(self, instance, validated_data):
        instance.price = instance.item.price
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def validate(self, attrs):
        if self.instance:
            if not self.context['request'].user.cart.cart_items.filter(id=self.instance.id).exists():
                raise ValidationError('Сan not change the cart item that exists in the order!')
        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_items', many=True)
    total_cost = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
