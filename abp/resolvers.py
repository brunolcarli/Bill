"""
Módulo contendo os métodos de resolução de objetos para as consultas GraphQL.
"""
from datetime import datetime
from abp.models import (Battle, League, Trainer, Score, Leader, Badge)
from abp.utils import validate_global_id


def resolve_leagues(**kwargs):
    """
    Resolve a consulta de ligas.
    """
    league_global_id = kwargs.get('id')
    if league_global_id:
        if 'id' in kwargs.keys():
            league_id = validate_global_id(kwargs.pop('id'), 'LeagueType')
            kwargs['id'] = league_id

    return League.objects.filter(**kwargs)


def resolve_trainers(**kwargs):
    """
    Resolve a consulta de treinadores.
    """
    if 'id' in kwargs.keys():
        trainer_id = validate_global_id(kwargs.pop('id'), 'TrainerType')
        kwargs['id'] = trainer_id

    return Trainer.objects.filter(**kwargs)


def resolve_leaders(**kwargs):
    """
    Resolve a consulta de líderes.
    """
    if 'id' in kwargs.keys():
        leader_id = validate_global_id(kwargs.pop('id'), 'LeaderType')
        kwargs['id'] = leader_id

    return Leader.objects.filter(**kwargs)


def resolve_scores(**kwargs):
    """
    Resolve a consulta de scores.
    """
    if 'league__id__in' in kwargs.keys():
        global_ids = kwargs.pop('league__id__in')
        league_ids = [validate_global_id(i, 'LeagueType') for i in global_ids]
        kwargs['league__id__in'] = league_ids

    if 'trainer__id__in' in kwargs.keys():
        global_ids = kwargs.pop('trainer__id__in')
        trainer_ids = [validate_global_id(i, 'TrainerType') for i in global_ids]
        kwargs['trainer__id__in'] = trainer_ids

    return Score.objects.filter(**kwargs)


def resolve_battles(**kwargs):
    """
    Resolve a consulta de battles.
    """
    if 'leader__id__in' in kwargs.keys():
        global_ids = kwargs.pop('leader__id__in')
        leader_ids = [validate_global_id(i, 'LeaderType') for i in global_ids]
        kwargs['leader__id__in'] = leader_ids

    if 'trainer__id__in' in kwargs.keys():
        global_ids = kwargs.pop('trainer__id__in')
        trainer_ids = [validate_global_id(i, 'TrainerType') for i in global_ids]
        kwargs['trainer__id__in'] = trainer_ids

    return Battle.objects.filter(**kwargs)


def resolve_standby(score_instance):
    """
    Um jogador ficará em standby (de molho) por 3 dias se tiver perdido a
    última batalha.
    """
    last_battle = score_instance.battles.last()
    # Se não houver uma última batalha é porque o jogador ainda não batalhou
    if not last_battle:
        return False
    if last_battle.winner_name != last_battle.trainer.discord_id:
        now = datetime.now()
        time_passed = now - last_battle.battle_datetime.replace(tzinfo=None)
        if time_passed.days < 3:
            return True
        return False

    return False