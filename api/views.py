from decimal import Decimal, InvalidOperation
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import JsonResponse, Http404, HttpResponseNotFound
import json

from db.models import ClubIndividualScore, ClubParticipation, ClubPointScore, ClubTimedScore, Season, SeasonCompetition, SeasonEvent, Team, TeamIndividualScore, TeamPointScore, TeamTimedScore

def authorize(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()


def seasonView(request):
    authorize(request)
    seasons = []
    for s in Season.objects.order_by("name"):
        seasons.append({
            'id': s.id,
            'name': s.name,
        })
    return JsonResponse(seasons, safe=False)


def competitionView(request, season_id):
    authorize(request)
    competitions = []
    for c in SeasonCompetition.objects.filter(season=season_id):
        competitions.append({
            'id': c.competition.id,
            'name': c.competition.name,
        })
    return JsonResponse(competitions, safe=False)


def clubView(request, season_id, competition_id):
    authorize(request)
    clubs = []
    for p in ClubParticipation.objects.filter(competition__season=season_id, competition__competition=competition_id):
        clubs.append({
            'id': p.club.id,
            'name': p.club.name,
        })
    return JsonResponse(clubs, safe=False)


def teamView(request, season_id, competition_id, club_id):
    authorize(request)
    teams = []
    for t in Team.objects.filter(club__competition__season=season_id, club__competition__competition=competition_id, club__club=club_id):
        teams.append({
            'id': t.id,
            'name': t.name,
        })
    return JsonResponse(teams, safe=False)


def eventView(request, season_id, competition_id):
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


def clubScoreView(request, season_id, competition_id, event_id, club_id):
    authorize(request)
    seasonEvent = None
    clubParticipation = None
    try:
        seasonEvent = SeasonEvent.objects.get(season=season_id, event=event_id)
        clubParticipation = ClubParticipation.objects.get(competition__season=season_id, competition__competition=competition_id, club=club_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    eventType = seasonEvent.event.type

    def getClubPoints():
        try:
            score = ClubPointScore.objects.get(event=seasonEvent.id, club=clubParticipation.id)
            return {
                'points': score.points,
            }
        except ObjectDoesNotExist:
            return {
                'points': None
            }
    def getClubIndividualPoints():
        scores = []
        for s in ClubIndividualScore.objects.filter(event=seasonEvent.id, club=clubParticipation.id):
            scores.append({
                'name': s.name,
                'points': s.points,
            })
        return scores
    def getClubTimed():
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

    def setClubPoints(score):
        points = score['points']
        if points != None:
            ClubPointScore.objects.update_or_create(
                event=seasonEvent.id,
                club=clubParticipation.id,
                defaults={'points': Decimal(points)},
            )
        else:
            ClubPointScore.objects.filter(
                event=seasonEvent.id,
                club=clubParticipation.id,
            ).delete()
    def setClubIndividualPoints():
        raise NotImplementedError
    def setClubTimed():
        time = score['time']
        errors = score['errors']
        if time != None and errors != None:
            ClubTimedScore.objects.update_or_create(
                event=seasonEvent.id,
                club=clubParticipation.id,
                defaults={'time': Decimal(time), 'errors': Decimal(errors)},
            )
        elif time == None and errors == None:
            ClubTimedScore.objects.filter(
                event=seasonEvent.id,
                club=clubParticipation.id,
            ).delete()

    def invalid():
        raise Http404

    if request.method != 'POST':
        result = [getClubPoints, invalid, getClubIndividualPoints, invalid, getClubTimed, invalid][eventType]()
        return JsonResponse(result, safe=False)
    else:
        try:
            score = json.loads(request.body.decode('utf-8'))
            [setClubPoints, invalid, setClubIndividualPoints, invalid, setClubTimed, invalid][eventType](score)
            return JsonResponse(True, safe=False)
        except:
            response = JsonResponse(False, safe=False)
            response.status_code = 400
            return response


def teamScoreView(request, season_id, competition_id, event_id, club_id, team_id):
    authorize(request)
    seasonEvent = None
    team = None
    try:
        seasonEvent = SeasonEvent.objects.get(season=season_id, event=event_id)
        team = Team.objects.get(id=team_id, club__competition__season=season_id, club__competition__competition=competition_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    eventType = seasonEvent.event.type

    def getTeamPoints():
        try:
            score = TeamPointScore.objects.get(event=seasonEvent.id, team=team.id)
            return {
                'points': score.points,
            }
        except ObjectDoesNotExist:
            return {
                'points': None
            }
    def getTeamIndividualPoints():
        scores = []
        for s in TeamIndividualScore.objects.filter(event=seasonEvent.id, team=team.id):
            scores.append({
                'name': s.name,
                'points': s.points,
            })
        return scores
    def getTeamTimed():
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

    def setTeamPoints(score):
        points = score['points']
        if points != None:
            TeamPointScore.objects.update_or_create(
                event=seasonEvent.id,
                team=team.id,
                defaults={'points': Decimal(points)},
            )
        else:
            TeamPointScore.objects.filter(
                event=seasonEvent.id,
                team=team.id,
            ).delete()
    def setTeamIndividualPoints():
        raise NotImplementedError
    def setTeamTimed():
        time = score['time']
        errors = score['errors']
        if time != None and errors != None:
            TeamTimedScore.objects.update_or_create(
                event=seasonEvent.id,
                team=team.id,
                defaults={'time': Decimal(time), 'errors': Decimal(errors)}
            )
        elif time == None and errors == None:
            TeamTimedScore.objects.filter(
                event=seasonEvent.id,
                team=team.id,
            ).delete()

    def invalid():
        raise Http404

    if request.method != 'POST':
        result = [invalid, getTeamPoints, invalid, getTeamIndividualPoints, invalid, getTeamTimed][eventType]()
        return JsonResponse(result, safe=False)

    else:
        try:
            score = json.loads(request.body.decode('utf-8'))
            [invalid, setTeamPoints, invalid, setTeamIndividualPoints, invalid, setTeamTimed][eventType](score)
            return JsonResponse(True, safe=False)
        except:
            response = JsonResponse(False, safe=False)
            response.status_code = 400
            return response
