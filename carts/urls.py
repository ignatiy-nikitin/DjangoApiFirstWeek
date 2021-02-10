from django.urls import path
from rest_framework.routers import DefaultRouter

from carts.views import CartRetrieveAPIView, CartItemViewSet

cart_router = DefaultRouter()
cart_router.register('items', CartItemViewSet, basename='cart_item')

urlpatterns = [
    path('', CartRetrieveAPIView.as_view(), name='cart')
]

urlpatterns += cart_router.urls
