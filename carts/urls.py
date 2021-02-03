from rest_framework.routers import DefaultRouter

from carts.views import CartListViewSet, CartItemViewSet

cart_router = DefaultRouter()
cart_router.register('items', CartItemViewSet, basename='cart_item')
cart_router.register('', CartListViewSet, basename='cart')
urlpatterns = cart_router.urls
