"""
Módulo contendo os métodos de resolução de objetos para as consultas GraphQL.
"""
from abp.models import (Battle, League, Trainer, Score, Leader, Badge)
from graphql_relay import from_global_id


def resolve_leagues(**kwargs):
    """
    Resolve a consulta de ligas.
    """
    league_global_id = kwargs.get('id')

    if league_global_id:
        kind, league_id = from_global_id(league_global_id)
        if not kind == 'LeagueType':
            raise Exception('The given ID is not a league ID!')

        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception('This league does not exists!')

        return [league]
    return League.objects.all()
