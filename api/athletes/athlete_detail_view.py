from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class AthleteDetailView(APIView):
    """
    View for interacting with an athlete by id
    """

    def get(self, request):
        """

        Args:
            request:

        Returns:

        """
        return Response({"message": "coming soon"})
