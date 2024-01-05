from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from accounts.serializers.user_serializer import UserSerializer


class CreateUserView(APIView):
    """Creates a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request):
        """Creates a new user by posting user data"""
        serializer = UserSerializer(instance=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
