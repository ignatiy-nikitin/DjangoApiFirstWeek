import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from items.models import Item
from orders.models import Order


class CartItemViewCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create()
        self.item = Item.objects.create(
            title='test item title',
            description='test desc',
            weight=random.randint(0, 1000),
            price=random.randint(0, 100_000)
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('cart:cart_item-list')

    def test_unauthorised(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test(self):
        data = {
            'quantity': 10,
            'item_id': self.item.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get()
        print(response.json())
        self.assertEqual(
            response.json(),
            {
                'id': cart_item.id,
                'item': {
                    'id': self.item.id,
                    'title': self.item.title,
                    'description': self.item.description,
                    'image': None,
                    'weight': self.item.weight,
                    'price': f'{self.item.price}.00',
                },
                'item_id': self.item.id,
                'quantity': data['quantity'],
                'price': f'{self.item.price}.00',
                'total_price': f'{self.item.price * data["quantity"]}.00'
            }
        )
        self.assertEqual(
            model_to_dict(cart_item),
            {
                'id': cart_item.id,
                'item': self.item.id,
                'cart': cart_item.cart.id,
                'quantity': data['quantity'],
                'price': Decimal(f'{self.item.price}.00'),
            }
        )


class CartItemViewListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create()
        self.cart = Cart.objects.create(user=self.user)
        self.items = [
            Item.objects.create(
                title=f'test item title {i}',
                description=f'test desc {i}',
                weight=random.randint(1, 1000),
                price=random.randint(1, 10000)
            ) for i in range(10)
        ]
        self.cart_items = []
        for _ in range(10):
            item = random.choice(self.items)
            self.cart_items.append(CartItem.objects.create(
                item=item,
                cart=self.cart,
                quantity=random.randint(0, 100),
                price=item.price,
            ))

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('cart:cart_item-list')

    def test_unauthorised(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(
            data['results'],
            [
                {
                    'id': cart_item.id,
                    'item': {
                        'id': cart_item.item.id,
                        'title': cart_item.item.title,
                        'description': cart_item.item.description,
                        'image': None,
                        'weight': cart_item.item.weight,
                        'price': f'{cart_item.item.price}.00',
                    },
                    'item_id': cart_item.item.id,
                    'quantity': cart_item.quantity,
                    'price': f'{cart_item.price}.00',
                    'total_price': f'{cart_item.total_price}.00'
                } for cart_item in self.cart_items[:len(data['results'])]
            ]
        )


class CartItemViewRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create()
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(
            title='test item title',
            description='test desc',
            weight=random.randint(1, 1000),
            price=random.randint(1, 10000)
        )
        self.cart_item = CartItem.objects.create(
            item=self.item,
            cart=self.cart,
            quantity=random.randint(0, 100),
            price=self.item.price,
        )
        self.url = reverse('cart:cart_item-detail', kwargs={'pk': self.cart_item.id})

    def test_unauthorised(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.cart_item.id,
                'item': {
                    'id': self.item.id,
                    'title': self.item.title,
                    'description': self.item.description,
                    'image': None,
                    'weight': self.item.weight,
                    'price': f'{self.item.price}.00',
                },
                'item_id': self.item.id,
                'quantity': self.cart_item.quantity,
                'price': f'{self.cart_item.price}.00',
                'total_price': f'{self.cart_item.total_price}.00',
            }
        )

    # def test_update_price_of_item(self):
    #     """Проверка изменения price и total_price у cart_item, при изменении price у item"""
    #     self.item.price = self.item.price + random.randint(0, 10)
    #     self.item.save()


class CartItemViewUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create()
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(
            title='test item title',
            description='test desc',
            weight=random.randint(1, 100),
            price=random.randint(1, 100)
        )
        self.cart_item = CartItem.objects.create(
            item=self.item,
            cart=self.cart,
            quantity=random.randint(0, 100),
            price=self.item.price,
        )
        self.url = reverse('cart:cart_item-detail', kwargs={'pk': self.cart_item.id})

    def test_unauthorised_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_unauthorised_patch(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_normal_update(self):
        self.client.force_authenticate(self.user)
        data = {
            'item_id': self.item.id,
            'quantity': self.cart_item.quantity + random.randint(0, 100),
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.cart_item.id,
                'item': {
                    'id': self.item.id,
                    'title': self.item.title,
                    'description': self.item.description,
                    'image': None,
                    'weight': self.item.weight,
                    'price': f'{self.item.price}.00',
                },
                'item_id': data['item_id'],
                'quantity': data['quantity'],
                'price': f'{self.cart_item.price}.00',
                'total_price': f'{data["quantity"] * self.cart_item.price}.00',
            }
        )

    def test_not_all_parameters(self):
        self.client.force_authenticate(self.user)
        data = {}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        fields_required_text = 'This field is required.'
        self.assertEqual(
            response.json(),
            {
                'item_id': [fields_required_text],
                'quantity': [fields_required_text],
            }
        )

    def test_update_cart_which_in_order(self):
        self.client.force_authenticate(self.user)
        Order.objects.create(
            recipient=self.user,
            address='some test address',
            cart=self.cart,
            total_cost=1000,
            delivery_dt='2021-02-11T13:24:01.570Z',
        )
        data = {
            'item_id': self.item.id,
            'quantity': self.cart_item.quantity + random.randint(0, 100),
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Сan not change the cart item that exists in the order!']})


class CartItemViewDeleteTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create()
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(
            title='test item title',
            description='test desc',
            weight=random.randint(1, 1000),
            price=random.randint(1, 10000)
        )
        self.cart_item = CartItem.objects.create(
            item=self.item,
            cart=self.cart,
            quantity=random.randint(0, 100),
            price=self.item.price,
        )
        self.url = reverse('cart:cart_item-detail', kwargs={'pk': self.cart_item.id})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertRaises(CartItem.DoesNotExist, CartItem.objects.get, id=self.cart_item.id)
