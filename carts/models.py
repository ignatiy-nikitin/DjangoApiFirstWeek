from django.conf import settings
from django.db import models

from items.models import Item


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    items = models.ManyToManyField(Item, through='CartItem', blank=True)

    @property
    def total_cost(self):
        return sum(self.cart_items.total_price)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    @property
    def total_price(self):
        return self.quantity * self.price
