from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.username
