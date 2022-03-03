from django.urls import path

from . import views

urlpatterns = [
    path('seasons', views.seasonView),
    path('seasons/<uuid:season_id>/competitions', views.competitionView),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/clubs', views.clubView),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/clubs/<uuid:club_id>/teams', views.teamView),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events', views.eventView),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events/<uuid:event_id>/clubs/<uuid:club_id>/scores', views.clubScoreView),
    path('seasons/<uuid:season_id>/competitions/<uuid:competition_id>/events/<uuid:event_id>/clubs/<uuid:club_id>/teams/<uuid:team_id>/scores', views.teamScoreView),
]
