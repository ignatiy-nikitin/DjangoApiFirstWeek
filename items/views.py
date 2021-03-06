from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter

from items.filters import ItemFilter
from items.models import Item
from items.paginations import ItemPageNumberPagination
from items.serializers import ItemSerializer


class ItemListRetrieveModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering = ['id']
    ordering_fields = ['price']
