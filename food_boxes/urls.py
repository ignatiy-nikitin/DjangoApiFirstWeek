from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from food_boxes import settings

schema_view = get_schema_view(
    openapi.Info(
        title='Stepic DRF API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_url = [
    path('users/', include('users.urls')),
    path('items/', include('items.urls')),
    path('carts/', include(('carts.urls', 'cart'))),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_url)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
