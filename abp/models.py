from django.db import models


class Quote(models.Model):
    """
    Defines a quote model to store a message.
    """
    quote = models.CharField(max_length=600, null=False, blank=False)


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
    gym_leaders = models.ManyToManyField(
        'abp.Leader',
        related_name='league_gym_leaders'
    )
    elite_four = models.ManyToManyField(
        'abp.Leader',
        related_name='league_elite_four'
    )
    competitors = models.ManyToManyField(
        'abp.Trainer',
        related_name='league_competitors'
    )
    champion = models.ForeignKey(
        'abp.Leader',
        on_delete=models.CASCADE,
        related_name='league_champion',
        null=True
    )
    winner = models.ForeignKey(
        'abp.Trainer',
        on_delete=models.CASCADE,
        related_name='league_winner',
        null=True
    )


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
    loose_percentage = models.FloatField(default=0)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)


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
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        null=True
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        null=True
    )
    battles = models.ManyToManyField('abp.Battle')
    badges = models.ManyToManyField('abp.Badge')


class Battle(models.Model):
    """
    Defines a battle between a leader and a trainer.
    The battles can be seen by an scoreboard.
    """
    battle_datetime = models.DateTimeField(auto_now_add=True)
    winner_name = models.CharField(max_length=100)
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        null=True,
        related_name='battling_trainer'
    )
    leader = models.ForeignKey(
        Leader,
        on_delete=models.CASCADE,
        null=True,
        related_name='battling_leader'
    )


class Badge(models.Model):
    """
    Defines a badge representing the victory of a trainer over a
    Gym Leader.
    """
    reference = models.CharField(max_length=100)
