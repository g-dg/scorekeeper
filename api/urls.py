from django.urls import path

from . import views

urlpatterns = [
    path('seasons', views.getSeasons),
    path('seasons/<uuid:season_id>/competitions', views.getSeasonCompetitions),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/clubs', views.getSeasonCompetitionClubs),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/clubs/<uuid:club_id>/teams', views.getSeasonCompetitionClubTeams),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events', views.getSeasonCompetitionEvents),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events/<uuid:event_id>/clubs/<uuid:club_id>/scores', views.getClubScores),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events/<uuid:event_id>/clubs/<uuid:club_id>/teams/<uuid:team_id>/scores', views.getTeamScores),
]
