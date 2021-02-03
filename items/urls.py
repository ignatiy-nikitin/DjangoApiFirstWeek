from rest_framework.routers import DefaultRouter

from items.views import ItemListRetrieveModelViewSet

item_router = DefaultRouter()
item_router.register('', ItemListRetrieveModelViewSet, basename='item')
urlpatterns = item_router.urls
