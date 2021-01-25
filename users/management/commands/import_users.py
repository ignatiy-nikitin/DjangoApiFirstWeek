import requests
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from users.models import User

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()

        for user in response:
            User.objects.update_or_create(
                id=user['id'],
                defaults={
                    'username': user['email'].split('@')[0],
                    'first_name': user['info']['name'],
                    'last_name': user['info']['surname'],
                    'middle_name': user['info']['patronymic'],
                    'email': user['email'],
                    'password': make_password(user['password']),
                    'address': user['city_kladr'],
                    'phone_number': user['contacts']['phoneNumber'],
                }
            )
