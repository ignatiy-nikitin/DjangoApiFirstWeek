import json

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from items.filters import ItemFilter
from items.models import Item
from items.paginations import ItemPageNumberPagination
from items.serializers import ItemSerializer

ITEM_CACHE_DATA = ''
ITEM_CACHE_TTL = 60 * 5


@receiver([post_save, post_delete], sender=Item)
def invalidate_user_cache(sender, **kwargs):
    cache.clear()


class ItemListRetrieveModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ItemPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering = ['id']
    ordering_fields = ['price']

    def list(self, request, *args, **kwargs):
        cached_response = cache.get(request.build_absolute_uri())
        if cached_response:
            return Response(json.loads(cached_response), status=status.HTTP_200_OK)
        else:
            response = super().list(request, *args, **kwargs)
            cache.set(request.build_absolute_uri(), json.dumps(response.data), ITEM_CACHE_TTL)
            return response
