from django.db import models


class Quote(models.Model):
    '''
       Defines a quote model to store a message.
    '''
    quote = models.CharField(max_length=600, null=False, blank=False)


class Season(models.Model):
    '''
        Defines a Season.
    '''
    reference = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    # TODO link to a tournament

    league = models.ForeignKey(
        'abp.League',
        on_delete=models.CASCADE,
        null=True
    )


class Tournament(models.Model):
    '''
        Defines a tournament
    '''
    name = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    # TODO link to season
    # TODO link to trainers


class League(models.Model):
    '''
        Defines a league.
    '''
    reference = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    # TODO link to season
    # TODO link to trainers


class Leader(models.Model):
    '''
        Defines a leader.
        A leader can be a gym leader, elite four or champion.
    '''
    ROLES = (
        ('Gym Leader', 'Gym Leader'),
        ('Elite Four', 'Elite Four'),
        ('Champion', 'Champion')
    )

    registration_date = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=25, null=False, blank=False)
    num_wins = models.IntegerField(default=0)
    num_losses = models.IntegerField(default=0)
    num_battles = models.IntegerField(default=0)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        null=False,
        blank=False
    )

    # TODO pokemon type
    # TODO link to league
    # TODO link to battles


class Trainer(models.Model):
    '''
        Defines a trainer.
    '''
    registration_date = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=25, null=False, blank=False)
    num_badges = models.IntegerField(default=0)
    num_wins = models.IntegerField(default=0)
    num_losses = models.IntegerField(default=0)
    num_battles = models.IntegerField(default=0)

    # TODO link to scores
    # TODO link to battles


class TrainerBattle(models.Model):
    '''
        Defines a battle between two trainers.
    '''
    battle_datetime = models.DateTimeField(auto_now_add=True)

    # TODO link to trainer 1 and 2
    # TODO link to winner (a trainer)


class LeagueBattle(models.Model):
    '''
        Defines a Battle between a trainer and a league leader.
    '''
    battle_datetime = models.DateTimeField(auto_now_add=True)
    winner_nickname = models.CharField(max_length=25, null=False, blank=False)
    # TODO link to trainer
    # TODO link to laeder


class LeagueScore(models.Model):
    '''
        Defines a trainer score based on an league.
    '''
    reference = models.CharField(max_length=100, null=False, blank=False)

    # TODO link to a league


class TournamentScore(models.Model):
    '''
        Defines a trainer score based on an tournament.
    '''
    reference = models.CharField(max_length=100, null=False, blank=False)

    # TODO link to a tournament
