"""
Módulo para ferramentas utili†arias.
"""
from graphql_relay import from_global_id


def validate_global_id(global_id, expected_type):
    """
    Valida um ID global mno formato ObjectType:IntId.
    Retorna o ID numérico se a operação suceder.
    Levanta exception se o ID fornecido não bater com o tipo esperado.
    param : global_id : <str>
    param : expected_type : <str>
    return : <int>
    """
    kind, int_value = from_global_id(global_id)
    if not kind == expected_type:
        raise Exception(f'The given ID is not a {expected_type} ID!')

    return int_value
