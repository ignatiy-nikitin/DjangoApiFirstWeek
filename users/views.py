from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer


class CurrentUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
