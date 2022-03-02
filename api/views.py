from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import JsonResponse, Http404, HttpResponseNotFound

from db.models import ClubIndividualScore, ClubParticipation, ClubPointScore, ClubTimedScore, Season, SeasonCompetition, SeasonEvent, Team, TeamIndividualScore, TeamPointScore, TeamTimedScore

def authorize(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()


def getSeasons(request):
    authorize(request)
    seasons = []
    for s in Season.objects.order_by("name"):
        seasons.append({
            'id': s.id,
            'name': s.name,
        })
    return JsonResponse(seasons, safe=False)


def getSeasonCompetitions(request, season_id):
    authorize(request)
    competitions = []
    for c in SeasonCompetition.objects.filter(season=season_id):
        competitions.append({
            'id': c.competition.id,
            'name': c.competition.name,
        })
    return JsonResponse(competitions, safe=False)


def getSeasonCompetitionClubs(request, season_id, competition_id):
    authorize(request)
    clubs = []
    for p in ClubParticipation.objects.filter(competition__season=season_id, competition__competition=competition_id):
        clubs.append({
            'id': p.club.id,
            'name': p.club.name,
        })
    return JsonResponse(clubs, safe=False)


def getSeasonCompetitionClubTeams(request, season_id, competition_id, club_id):
    authorize(request)
    teams = []
    for t in Team.objects.filter(club__competition__season=season_id, club__competition__competition=competition_id, club__club=club_id):
        teams.append({
            'id': t.id,
            'name': t.name,
        })
    return JsonResponse(teams, safe=False)


def getSeasonCompetitionEvents(request, season_id, competition_id):
    authorize(request)
    events = []
    for e in SeasonEvent.objects.filter(season=season_id, event__competition=competition_id):
        events.append({
            'id': e.event.id,
            'name': e.event.name,
            'type': {
                'groupType': 'club' if e.event.type in [0, 2, 4] else 'team',
                'scoreType': 'points' if e.event.type in [0, 1, 2, 3] else 'timed',
                'multiple': e.event.type in [2, 3],
            },
        })
    return JsonResponse(events, safe=False)


def getClubScores(request, season_id, competition_id, event_id, club_id):
    authorize(request)
    seasonEvent = None
    clubParticipation = None
    try:
        seasonEvent = SeasonEvent.objects.get(season=season_id, event=event_id)
        clubParticipation = ClubParticipation.objects.get(competition__season=season_id, competition__competition=competition_id, club=club_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    eventType = seasonEvent.event.type
    def clubPoints():
        try:
            score = ClubPointScore.objects.get(event=seasonEvent.id, club=clubParticipation.id)
            return {
                'points': score.points,
            }
        except ObjectDoesNotExist:
            return {
                'points': None
            }
    def clubIndividualPoints():
        scores = []
        for s in ClubIndividualScore.objects.filter(event=seasonEvent.id, club=clubParticipation.id):
            scores.append({
                'name': s.name,
                'points': s.points,
            })
        return scores
    def clubTimed():
        try:
            score = ClubTimedScore.objects.get(event=seasonEvent.id, club=clubParticipation.id)
            return {
                'time': score.time,
                'errors': score.errors,
            }
        except ObjectDoesNotExist:
            return {
                'time': None,
                'errors': None,
            }
    def invalid():
        raise Http404
    result = [clubPoints, invalid, clubIndividualPoints, invalid, clubTimed, invalid][eventType]()

    return JsonResponse(result, safe=False)


def getTeamScores(request, season_id, competition_id, event_id, club_id, team_id):
    authorize(request)
    seasonEvent = None
    team = None
    try:
        seasonEvent = SeasonEvent.objects.get(season=season_id, event=event_id)
        team = Team.objects.get(id=team_id, club__competition__season=season_id, club__competition__competition=competition_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    eventType = seasonEvent.event.type
    def teamPoints():
        try:
            score = TeamPointScore.objects.get(event=seasonEvent.id, team=team.id)
            return {
                'points': score.points,
            }
        except ObjectDoesNotExist:
            return {
                'points': None
            }
    def teamIndividualPoints():
        scores = []
        for s in TeamIndividualScore.objects.filter(event=seasonEvent.id, team=team.id):
            scores.append({
                'name': s.name,
                'points': s.points,
            })
        return scores
    def teamTimed():
        try:
            score = TeamTimedScore.objects.get(event=seasonEvent.id, team=team.id)
            return {
                'time': score.time,
                'errors': score.errors,
            }
        except ObjectDoesNotExist:
            return {
                'time': None,
                'errors': None,
            }
    def invalid():
        raise Http404
    result = [invalid, teamPoints, invalid, teamIndividualPoints, invalid, teamTimed][eventType]()

    return JsonResponse(result, safe=False)

