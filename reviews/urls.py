from rest_framework.routers import DefaultRouter

from reviews.views import ReviewVewSet

review_router = DefaultRouter()
review_router.register('', ReviewVewSet, basename='review')

urlpatterns = review_router.urls
