from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.serializers.user_serializer import UserSerializer


class UserListView(APIView):
    """View for interacting with the user without id"""
    serializer_class = UserSerializer

    def post(self, request):
        """
        Endpoint for creating a new user
        Args:
            request:

        Returns:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
