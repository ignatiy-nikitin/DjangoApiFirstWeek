from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer


class CartListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
