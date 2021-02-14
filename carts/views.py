from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from carts.models import CartItem
from carts.serializers import CartSerializer, CartItemSerializer


class CartRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CartItem, cart__user=self.request.user, id=self.kwargs['pk'])

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.cart.cart_items.all()
