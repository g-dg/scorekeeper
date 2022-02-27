from django.contrib import admin

from .models import Club, Season, Competition, SeasonCompetition, ClubParticipation, Team, Event, SeasonEvent, ClubPointScore, TeamPointScore, ClubTimedScore, TeamTimedScore, ClubIndividualScore, TeamIndividualScore

admin.site.site_header = 'Garnet DeGelder\'s Score Tracker Administration'
admin.site.site_title = 'Garnet DeGelder\'s Score Tracker'


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
	ordering = ['name']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
	ordering = ['name']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	ordering = ['name']


@admin.register(SeasonCompetition)
class SeasonCompetitionAdmin(admin.ModelAdmin):
	ordering = ['season__name', 'competition__name']


@admin.register(ClubParticipation)
class ClubParticipationAdmin(admin.ModelAdmin):
	ordering = ['club__name', 'competition__season__name', 'competition__competition__name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	ordering = ['club__club__name', 'club__competition__season__name', 'club__competition__competition__name', 'name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	ordering = ['competition__name', 'name']


@admin.register(SeasonEvent)
class SeasonEventAdmin(admin.ModelAdmin):
	ordering = ['season__name', 'event__competition__name', 'event__name']


# @admin.register(ClubPointScore)
# class ClubPointScoreAdmin(admin.ModelAdmin):
# 	pass


# @admin.register(TeamPointScore)
# class TeamPointScoreAdmin(admin.ModelAdmin):
# 	pass


# @admin.register(ClubTimedScore)
# class ClubTimedScoreAdmin(admin.ModelAdmin):
# 	pass


# @admin.register(TeamTimedScore)
# class TeamTimedScoreAdmin(admin.ModelAdmin):
# 	pass


# @admin.register(ClubIndividualScore)
# class ClubIndividualScoreAdmin(admin.ModelAdmin):
# 	pass


# @admin.register(TeamIndividualScore)
# class TeamIndividualScoreAdmin(admin.ModelAdmin):
# 	pass
