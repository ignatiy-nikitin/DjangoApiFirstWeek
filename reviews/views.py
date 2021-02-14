from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewVewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        permissions = []
        if self.action in ('create',):
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]
