from django.urls import path

from .athletes.athlete_detail_view import AthleteDetailView
from .athletes.athlete_list_view import AthleteListView

app_name = "api"

urlpatterns = [
    path("athlete/", AthleteListView.as_view(), name="athlete-list"),
    path("athlete/<int:id>/", AthleteDetailView.as_view(), name="athlete-details"),
]
