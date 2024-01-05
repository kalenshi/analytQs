from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class AthleteListView(APIView):
    """
    List the athlete
    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        return Response({"message": "Athletes coming soon"})
