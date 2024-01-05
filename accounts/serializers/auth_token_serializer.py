from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        # The user might deliberately have a white space at the end of their password
    )

    def validate(self, attrs):
        """
        Validates the incoming attributes of the usr
        Args:
            attrs:

        Returns:

        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            message = _("Unable to authenticate User")
            raise serializers.ValidationError(message, code="authorization")

        attrs["user"] = user
        return attrs
