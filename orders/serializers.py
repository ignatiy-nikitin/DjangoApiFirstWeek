from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from carts.serializers import CartSerializer
from orders.models import Order


class OrderListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'cart', 'status', 'total_cost', 'address', 'delivery_dt', 'created_dt']
        read_only_fields = ['id', 'cart', 'status', 'total_cost', 'created_dt']
        extra_kwargs = {
            'address': {'required': True},
            'delivery_dt': {'required': True},
        }

    def create(self, validated_data):
        order = Order(
            delivery_dt=validated_data['delivery_dt'],
            recipient=self.context['request'].user,
            address=validated_data['address'],
            cart=self.context['request'].user.cart,
            total_cost=self.context['request'].user.cart.total_cost,
        )
        order.save()
        return order

    def validate_delivery_dt(self, value):
        if value <= timezone.now():
            raise ValidationError('Delivery date must be greater than the current date!')
        return value

    def validate(self, attrs):
        if not self.context['request'].user.cart.cart_items.count():
            raise ValidationError('The cart must contain at least one item!')
        return attrs


class OrderRetrieveUpdateSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'cart', 'status', 'recipient', 'total_cost', 'address', 'delivery_dt', 'created_dt']
        read_only_fields = ['id', 'recipient', 'total_cost', 'created_dt']

    def update(self, instance, validated_data):
        if validated_data.get('status'):
            instance.status = validated_data['status']
            instance.save()
            return instance
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

    def validate(self, attrs):
        if self.instance:
            if self.instance.status != 'created':
                raise ValidationError('Cannot modify orders with a status other than "created"!')
        return attrs

    def validate_status(self, value):
        if value != 'cancelled':
            raise ValidationError('Order can only be changed to "cancelled" status!')
        return value

    def validate_delivery_dt(self, value):
        if value <= timezone.now():
            raise ValidationError('Delivery date must be greater than the current date!')
        return value
