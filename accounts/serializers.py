"""
Serializers for the users API view
"""
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (get_user_model, authenticate, login)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model
    """

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8}
        }

    def create(self, validated_data):
        """
        Creates  and returns a user
        Args:
            validated_data (dict): key value pairs for the user attributes

        Returns:
            obj : User instance
        """
        return get_user_model().objects.create_user(**validated_data)
