"""
Módulo para ferramentas utili†arias.
"""
from math import ceil
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


def next_lv(level):
    """
    Fórmula para avançar de nível.
    """
    return ceil((4 *(level ** 3)) / 5)


def get_exp(trainer_lv, leader_lv):
    """
    Retorna a quantidade de exp apos uma batalha.
    A exp depende do lv dos treinadores envolvidos.
    """
    return ceil((2 * leader_lv * (trainer_lv * 1.5)))


def lv_update(trainer):
    """
    Atualiza o lv e experiência do treinador/lider.
    """
    while trainer.exp >= trainer.next_lv:
        trainer.lv += 1
        trainer.next_lv = next_lv(trainer.lv)
