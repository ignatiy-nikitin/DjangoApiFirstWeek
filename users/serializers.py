from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'middle_name', 'phone_number',
                  'address']
        read_only_fields = ['id', 'username']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['email'].split('@')[0],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        if validated_data.get('email'):
            instance.username = validated_data['email'].split('@')[0]
            instance.email = validated_data['email']
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('address', instance.phone_number)
        instance.save()
        return instance
