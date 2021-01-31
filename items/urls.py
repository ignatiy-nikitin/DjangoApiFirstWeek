from django.urls import path

from items.views import get_view_item

urlpatterns = [
    path('<pk>', get_view_item)
]
