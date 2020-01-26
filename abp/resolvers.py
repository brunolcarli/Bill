"""
Módulo contendo os métodos de resolução de objetos para as consultas GraphQL.
"""
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
