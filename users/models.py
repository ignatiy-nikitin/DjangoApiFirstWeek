from django.contrib.auth.models import AbstractUser
from django.db import models

from carts.models import Cart
from orders.models import Order


class User(AbstractUser):
    middle_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    @property
    def cart(self):
        try:
            cart = Cart.objects.get(user=self, orders=None)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self)
        return cart
