from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import OrderListCreateSerializer, OrderRetrieveUpdateSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return OrderListCreateSerializer
        return OrderRetrieveUpdateSerializer

    def get_queryset(self):
        return self.request.user.orders.all()

    def get_object(self):
        return get_object_or_404(self.request.user.orders, pk=self.kwargs['pk'])
