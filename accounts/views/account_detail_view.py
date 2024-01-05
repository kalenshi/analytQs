from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from accounts.serializers.user_serializer import UserSerializer


class AccountDetailView(APIView):
    """
    Class responsible for the user details
    """
    serializer_class = UserSerializer

    def get_object(self, pk):
        """
        Retrieve the object with the provided primary key
        Args:
            pk(int): User id

        Returns:
            User: user object or 404
        """
        return get_object_or_404(get_user_model(), pk=pk)

    def get(self, request, user_id):
        """
        Retrieve the information of the user with the provided user id
        Args:
            request (object): request object
            user_id(int):User id of the account information

        Returns:
            HttpResponse:
        """
        user_information = self.get_object(pk=user_id)
        serializer = self.serializer_class(instance=user_information)

        return Response(serializer.data, status=status.HTTP_200_OK)
