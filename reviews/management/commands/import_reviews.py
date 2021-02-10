from datetime import datetime

import requests
from django.core.management.base import BaseCommand

from reviews.models import Review
from users.models import User

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()
        date_format = '%Y-%m-%d'

        for review in response:
            obj, _ = Review.objects.update_or_create(
                id=review['id'],
                defaults={
                    'author': User.objects.get(id=review['author']),
                    'text': review['content'],
                    'status': review['status']
                }
            )

            if review['created_at']:
                obj.created_at = datetime.strptime(review['created_at'], date_format).date()
                obj.save()
            if review['published_at']:
                obj.published_at = datetime.strptime(review['published_at'], date_format).date()
                obj.save()
