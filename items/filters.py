from django_filters import rest_framework as filters

from items.models import Item


class ItemFilter(filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['gt', 'gte', 'lt', 'lte', 'gt'],
            'weight': ['gt', 'gte', 'lt', 'lte', 'gt'],
        }
