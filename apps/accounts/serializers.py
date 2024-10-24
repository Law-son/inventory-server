from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not returned in the response
        }

    def create(self, validated_data):
        # Ensure the password is hashed before saving
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Only pop if the password key exists
        if 'password' in data:
            data.pop('password')  # Exclude password from representation
        return data
