from django.db import models

from food_boxes.settings import MEDIA_ITEM_IMAGE_DIR


class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to=MEDIA_ITEM_IMAGE_DIR)
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
