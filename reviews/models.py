from django.conf import settings
from django.db import models


class Reviews(models.Model):
    STATUS_CHOICES = [
        ('moderation', 'на модерации'),
        ('published', 'опубликован'),
        ('rejected', 'отклонен'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES)

    def __str__(self):
        return self.author
