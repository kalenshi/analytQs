"""
Serializers for the users API view
"""
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers

MINIMUM_PASSWORD_LENGTH = 8


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
            "password": {"write_only": True, "min_length": MINIMUM_PASSWORD_LENGTH}
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

    def update(self, instance, validated_data):
        """
        Method for updating only the email and/or password of the user
        Args:
            instance(obj): user model instance
            validated_data (dict): key/value pairs of user data

        Returns:
            obj: user instance that's been updated
        """
        password = validated_data.pop("password", None)
        user = super().update(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
