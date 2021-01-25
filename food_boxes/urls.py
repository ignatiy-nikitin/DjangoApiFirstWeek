from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from food_boxes import settings


api_url = [
    path('item/', include('items.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_url))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
