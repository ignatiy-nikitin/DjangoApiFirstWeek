from django.conf import settings
from django.db import models

from items.models import Item


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    items = models.ManyToManyField(Item, through='CartItem', blank=True)

    @property
    def total_cost(self):
        return sum([cart_item.total_price for cart_item in self.cart_items.all()])

    def __str__(self):
        return f'Cart {self.pk} of user {self.user.username}'


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'CartItem {self.pk} of cart {self.cart.pk}'

    @property
    def total_price(self):
        return self.quantity * self.price
