from rest_framework import serializers

from reviews.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'status', 'text', 'created_at', 'published_at']
        read_only_fields = ['id', 'status', 'created_at', 'published_at']

    def create(self, validated_data):
        review = Review(**validated_data)
        review.author = self.context['request'].user
        review.save()
        return review
