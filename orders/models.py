from django.conf import settings
from django.db import models

from carts.models import Cart


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'создан'),
        ('delivered', 'доставлен'),
        ('processed', 'в процессе'),
        ('cancelled', 'отменен'),
    ]

    created_dt = models.DateTimeField(auto_now_add=True)
    delivery_dt = models.DateTimeField()
    recipient = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=256)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='created')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Order of user {self.recipient.username}'
