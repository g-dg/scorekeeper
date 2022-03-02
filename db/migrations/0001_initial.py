# Generated by Django 3.2

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClubParticipation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('disqualified', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.club')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(0, 'Club Points'), (1, 'Team Points'), (2, 'Club Individual Points'), (3, 'Team Individual Points'), (4, 'Club Timed'), (5, 'Team Timed')], default=1)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.competition')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeasonEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('competition_overall_map_from_min', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('competition_overall_map_from_max', models.DecimalField(decimal_places=6, max_digits=15)),
                ('competition_overall_map_to_min', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('competition_overall_map_to_max', models.DecimalField(decimal_places=6, max_digits=15)),
                ('timed_time_min', models.DecimalField(decimal_places=6, max_digits=15, null=True)),
                ('timed_time_max', models.DecimalField(decimal_places=6, max_digits=15, null=True)),
                ('timed_time_points', models.DecimalField(decimal_places=6, max_digits=15, null=True)),
                ('timed_error_max', models.DecimalField(decimal_places=6, max_digits=15, null=True)),
                ('timed_error_points', models.DecimalField(decimal_places=6, max_digits=15, null=True)),
                ('constrain_points', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.event')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.season')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('disqualified', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.clubparticipation')),
            ],
        ),
        migrations.CreateModel(
            name='TeamTimedScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DecimalField(decimal_places=6, max_digits=15)),
                ('errors', models.DecimalField(decimal_places=6, max_digits=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPointScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('points', models.DecimalField(decimal_places=6, max_digits=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamIndividualScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('points', models.DecimalField(decimal_places=6, max_digits=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.team')),
            ],
        ),
        migrations.CreateModel(
            name='SeasonCompetition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('season_overall_map_from_min', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('season_overall_map_from_max', models.DecimalField(decimal_places=6, max_digits=15)),
                ('season_overall_map_to_min', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('season_overall_map_to_max', models.DecimalField(decimal_places=6, max_digits=15)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.competition')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.season')),
            ],
        ),
        migrations.CreateModel(
            name='ClubTimedScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DecimalField(decimal_places=6, max_digits=15)),
                ('errors', models.DecimalField(decimal_places=6, max_digits=15)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.clubparticipation')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
            ],
        ),
        migrations.CreateModel(
            name='ClubPointScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('points', models.DecimalField(decimal_places=6, max_digits=15)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.clubparticipation')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
            ],
        ),
        migrations.AddField(
            model_name='clubparticipation',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasoncompetition'),
        ),
        migrations.CreateModel(
            name='ClubIndividualScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('points', models.DecimalField(decimal_places=6, max_digits=15)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.clubparticipation')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.seasonevent')),
            ],
        ),
        migrations.AddConstraint(
            model_name='teamtimedscore',
            constraint=models.UniqueConstraint(fields=('event', 'team'), name='unique_TeamTimedScore_event_team'),
        ),
        migrations.AddConstraint(
            model_name='teampointscore',
            constraint=models.UniqueConstraint(fields=('event', 'team'), name='unique_TeamPointScore_event_team'),
        ),
        migrations.AddConstraint(
            model_name='teamindividualscore',
            constraint=models.UniqueConstraint(fields=('event', 'team', 'name'), name='unique_TeamIndividualScore_event_team_name'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('club', 'name'), name='unique_Team_club_name'),
        ),
        migrations.AddConstraint(
            model_name='seasonevent',
            constraint=models.UniqueConstraint(fields=('season', 'event'), name='unique_SeasonEvent_season_event'),
        ),
        migrations.AddConstraint(
            model_name='seasoncompetition',
            constraint=models.UniqueConstraint(fields=('season', 'competition'), name='unique_SeasonCompetition_season_competition'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('competition', 'name'), name='unique_Event_competition_name'),
        ),
        migrations.AddConstraint(
            model_name='clubtimedscore',
            constraint=models.UniqueConstraint(fields=('event', 'club'), name='unique_ClubTimedScore_event_club'),
        ),
        migrations.AddConstraint(
            model_name='clubpointscore',
            constraint=models.UniqueConstraint(fields=('event', 'club'), name='unique_ClubPointScore_event_club'),
        ),
        migrations.AddConstraint(
            model_name='clubparticipation',
            constraint=models.UniqueConstraint(fields=('club', 'competition'), name='unique_ClubParticipation_club_competition'),
        ),
        migrations.AddConstraint(
            model_name='clubindividualscore',
            constraint=models.UniqueConstraint(fields=('event', 'club', 'name'), name='unique_ClubIndividualScore_event_club_name'),
        ),
    ]
