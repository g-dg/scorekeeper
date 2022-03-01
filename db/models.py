from django.db import models
import uuid

# defines a club (group of teams)
class Club(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, unique=True)

	class Meta():
		pass

	def __str__(self):
		return self.name


# defines a season
class Season(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, unique=True)

	class Meta():
		pass

	def __str__(self):
		return self.name


# defines a competition
class Competition(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, unique=True)

	class Meta():
		pass

	def __str__(self):
		return self.name


# defines each competition in a particular season
class SeasonCompetition(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	season = models.ForeignKey(Season, on_delete=models.CASCADE)
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
	season_overall_map_from_min = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
	season_overall_map_from_max = models.DecimalField(max_digits=15, decimal_places=6)
	season_overall_map_to_min = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
	season_overall_map_to_max = models.DecimalField(max_digits=15, decimal_places=6)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_SeasonCompetition_season_competition', fields=['season', 'competition'])
		]

	def __str__(self):
		return '{} | {}'.format(self.season, self.competition)


# defines which competition seasons each club competes in
class ClubParticipation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	club = models.ForeignKey(Club, on_delete=models.CASCADE)
	competition = models.ForeignKey(SeasonCompetition, on_delete=models.CASCADE)
	disqualified = models.BooleanField(default=False)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_ClubParticipation_club_competition', fields=['club', 'competition'])
		]

	def __str__(self):
		return '{} | {}'.format(self.competition, self.club)


# defines a team
class Team(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	club = models.ForeignKey(ClubParticipation, on_delete=models.CASCADE)
	disqualified = models.BooleanField(default=False)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_Team_club_name', fields=['club', 'name'])
		]

	def __str__(self):
		return '{} | {}'.format(self.club, self.name)


# defines an event in a competition
class Event(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_Event_competition_name', fields=['competition', 'name'])
		]
	
	def __str__(self):
		return '{} | {}'.format(self.competition, self.name)


# defines an event of a competition in a particular season
class SeasonEvent(models.Model):
	class EventType(models.IntegerChoices):
		POINTS_CLUB = 0 # one set of points per club
		POINTS_TEAM = 1 # one set of points per team
		INDIVIDUAL_POINTS_CLUB = 2 # multiple sets of points per club, no team scores (if no entries, then 0 points for event, competition, and season)
		INDIVIDUAL_POINTS_TEAM = 3 # multiple sets of points per team (if no entries, then 0 points for event, competition, and season)
		TIMED_CLUB = 4 # one set of points per club, made by combining speed and accuracy points
		TIMED_TEAM = 5 # one set of points per team, made by combining speed and accuracy points

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	season = models.ForeignKey(Season, on_delete=models.CASCADE)
	competition_overall_map_from_min = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
	competition_overall_map_from_max = models.DecimalField(max_digits=15, decimal_places=6)
	competition_overall_map_to_min = models.DecimalField(max_digits=15, decimal_places=6, default=0.0)
	competition_overall_map_to_max = models.DecimalField(max_digits=15, decimal_places=6)
	timed_time_min = models.DecimalField(max_digits=15, decimal_places=6, null=True) # full speed points for anything equal to or under this duration
	timed_time_max = models.DecimalField(max_digits=15, decimal_places=6, null=True) # no speed points for anything over this duration
	timed_time_points = models.DecimalField(max_digits=15, decimal_places=6, null=True) # number of overall event points that the time is mapped to
	timed_error_max = models.DecimalField(max_digits=15, decimal_places=6, null=True) # maximum number of errors, no accuracy points if equal to or over this amount
	timed_error_points = models.DecimalField(max_digits=15, decimal_places=6, null=True) # number of overall event points that the accuracy points are mapped to
	constrain_points = models.BooleanField(default=True) # whether to constrain points between competition overall min and max (for timed events, this is also done while mapping the time to speed points)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_SeasonEvent_season_event', fields=['season', 'event'])
		]

	def __str__(self):
		return '{} | {}'.format(self.season, self.event)


class ClubPointScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	club = models.ForeignKey(ClubParticipation, on_delete=models.CASCADE)
	points = models.DecimalField(max_digits=15, decimal_places=6)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_ClubPointScore_event_club', fields=['event', 'club'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.club)


class TeamPointScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	points = models.DecimalField(max_digits=15, decimal_places=6)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_TeamPointScore_event_team', fields=['event', 'team'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.team)


class ClubTimedScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	club = models.ForeignKey(ClubParticipation, on_delete=models.CASCADE)
	time = models.DecimalField(max_digits=15, decimal_places=6) # time in seconds
	errors = models.DecimalField(max_digits=15, decimal_places=6) # number of errors

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_ClubTimedScore_event_club', fields=['event', 'club'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.club)


class TeamTimedScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	time = models.DecimalField(max_digits=15, decimal_places=6) # time in seconds
	errors = models.DecimalField(max_digits=15, decimal_places=6) # number of errors

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_TeamTimedScore_event_team', fields=['event', 'team'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.team)


class ClubIndividualScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	club = models.ForeignKey(ClubParticipation, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	points = models.DecimalField(max_digits=15, decimal_places=6)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_ClubIndividualScore_event_club_name', fields=['event', 'club', 'name'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.club)


class TeamIndividualScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(SeasonEvent, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	points = models.DecimalField(max_digits=15, decimal_places=6)

	class Meta():
		constraints = [
			models.UniqueConstraint(name='unique_TeamIndividualScore_event_team_name', fields=['event', 'team', 'name'])
		]

	def __str__(self):
		return '{} | {}'.format(self.event, self.team)

