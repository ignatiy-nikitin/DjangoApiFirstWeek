import os
import urllib.request

import requests
from django.core.management.base import BaseCommand

from food_boxes.settings import MEDIA_ROOT, MEDIA_ITEM_IMAGE_DIR
from items.models import Item

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()

        for item in response:
            image_url = item['image']
            image_name = item['image'].split('/')[-1]
            path = os.path.join(MEDIA_ROOT, MEDIA_ITEM_IMAGE_DIR)
            os.makedirs(path, exist_ok=True)
            urllib.request.urlretrieve(image_url, os.path.join(path, image_name))

            Item.objects.update_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'description': item['description'],
                    'image': os.path.join(MEDIA_ITEM_IMAGE_DIR, image_name),
                    'weight': item['weight_grams'],
                    'price': item['price'],
                }
            )
