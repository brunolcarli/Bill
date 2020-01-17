from django.db import models


class Quote(models.Model):
    """
    Defines a quote model to store a message.
    """
    quote = models.CharField(max_length=600, null=False, blank=False)


# class Season(models.Model):
#     '''
#         Defines a Season.
#     '''
#     reference = models.CharField(
#         max_length=100,
#         null=False,
#         blank=False,
#         unique=True
#     )
#     start_date = models.DateField()
#     end_date = models.DateField()
#     description = models.TextField()
#     season_tournaments = models.ManyToManyField(
#         'abp.Tournament'
#     )
#     season_league = models.ForeignKey(
#         'abp.League',
#         on_delete=models.CASCADE,
#         null=True
#     )


# class Tournament(models.Model):
#     '''
#         Defines a tournament
#     '''
#     name = models.CharField(
#         max_length=100,
#         null=False,
#         blank=False,
#         unique=True
#     )
#     start_date = models.DateField()
#     end_date = models.DateField()
#     description = models.TextField()
#     tournament_season = models.ForeignKey(
#         'abp.Season',
#         on_delete=models.CASCADE,
#     )
#     tournament_trainers = models.ManyToManyField(
#         'abp.Trainer'
#     )


class League(models.Model):
    """
    Defines a league.
    """
    reference = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # Gym leaders
    # elite four
    # champio
    # Competitors
    # winner


class Trainer(models.Model):
    """
    Defines a trainer.
    """
    name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        unique=True
    )
    join_date = models.DateTimeField(auto_now_add=True)

    battle_counter = models.IntegerField(default=0)
    badge_counter = models.IntegerField(default=0)
    leagues_counter = models.IntegerField(default=0)
    win_percentage = models.FloatField(default=0)
    loose_battles = models.FloatField(default=0)

    # TODO link to scores


class Leader(Trainer):
    """
    Defines a leader.
    A leader can be a gym leader, elite four or champion.
    """
    ROLES = (
        ('Gym Leader', 'Gym Leader'),
        ('Elite Four', 'Elite Four'),
        ('Champion', 'Champion')
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        null=False,
        blank=False
    )
    pokemon_type = models.CharField(max_length=100)
    clauses = models.TextField(blank=True, null=True)


class Score(models.Model):
    """
    A score is a league board containing the battles, wint and loss times of a
    trainer or leader participating in that league.
    """
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    # trainer
    # battles
    # league


class Battle(models.Model):
    """
    Defines a battle between a leader and a trainer.
    The battles can be seen by an scoreboard.
    """
    battle_datetime = models.DateTimeField(auto_now_add=True)
    winner_global_id = models.CharField(max_length=100)
    # traineer
    # leader

# class TrainerBattle(models.Model):
#     '''
#         Defines a battle between two trainers.
#     '''
#     battle_datetime = models.DateTimeField(auto_now_add=True)

#     trainer_red_id = models.IntegerField()
#     trainer_blue_id = models.IntegerField()
#     winner_id = models.IntegerField()


# class LeagueBattle(models.Model):
#     '''
#         Defines a Battle between a trainer and a league leader.
#     '''
#     battle_datetime = models.DateTimeField(auto_now_add=True)
#     winner_id = models.IntegerField()
#     battling_trainer = models.ForeignKey(
#         'abp.Trainer',
#         on_delete=models.CASCADE,
#     )
#     battling_leader = models.ForeignKey(
#         'abp.Leader',
#         on_delete=models.CASCADE,
#     )


# class LeagueScore(models.Model):
#     '''
#         Defines a trainer score based on an league.
#     '''
#     class Meta:
#         unique_together = [['league_reference', 'trainer_reference']]

#     reference = models.CharField(
#         max_length=100,
#         null=False,
#         blank=False,
#         unique=True
#     )
#     league_reference = models.ForeignKey(
#         'abp.League',
#         on_delete=models.CASCADE,
#     )
#     trainer_reference = models.ForeignKey(
#         'abp.Trainer',
#         on_delete=models.CASCADE
#     )


# class TournamentScore(models.Model):
#     '''
#         Defines a trainer score based on an tournament.
#     '''
#     class Meta:
#         unique_together = [['tournament_reference', 'trainer_reference']]

#     reference = models.CharField(
#         max_length=100,
#         null=False,
#         blank=False,
#         unique=True
#     )
#     tournament_reference = models.ForeignKey(
#         'abp.Tournament',
#         on_delete=models.CASCADE,
#     )
#     trainer_reference = models.ForeignKey(
#         'abp.Trainer',
#         on_delete=models.CASCADE,
#         null=True
#     )
#     battles = models.ManyToManyField(TrainerBattle)
