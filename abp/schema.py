from math import ceil
import graphene
from abp.models import (Battle, League, Trainer, Score, Leader, Badge)
from graphql_relay import from_global_id
from abp.resolvers import (resolve_leagues, resolve_trainers, resolve_leaders,
                           resolve_scores, resolve_battles)
from abp.utils import get_exp, lv_update


#######################################################
#                  Enums
#######################################################
class PokemonTypes(graphene.Enum):
    """
    Defines the pokemon type the leader uses.
    The All type means the leader can use all pokémon types,
    usually the champion uses all pokémon types.
    """
    NORMAL = 'Normal'
    FIRE = 'Fire'
    WATER ='Water'
    GRASS = 'Grass'
    ELECTRIC = 'Electric'
    ICE = 'Ice'
    FIGHTING = 'Fighting'
    POISON = 'Poison'
    GROUND = 'Ground'
    FLYING = 'Flying'
    PSYCHIC = 'Psychic'
    BUG = 'Bug'
    ROCK = 'Rock'
    GHOST = 'Ghost'
    DARK = 'Dark'
    DRAGON = 'Dragon'
    STEEL = 'Steel'
    FAIRY = 'Fairy'
    ALL = 'All'


class Role(graphene.Enum):
    """
    League Roles
    """
    GYM_LEADER = 'Gym Leader'
    ELITE_FOUR = 'Elite Four'
    CHAMPION = 'Champion'


#######################################################
#                  GraphQL Types
#######################################################

class LeagueType(graphene.ObjectType):
    """
    Defines a graphQL serializer object for the League Model.
    """
    reference = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()
    gym_leaders = graphene.relay.ConnectionField('abp.schema.LeaderConnection')
    elite_four = graphene.relay.ConnectionField('abp.schema.LeaderConnection')
    champion = graphene.Field('abp.schema.LeaderType')
    competitors = graphene.relay.ConnectionField('abp.schema.TrainerConnection')
    winner = graphene.Field('abp.schema.TrainerType')

    def resolve_gym_leaders(self, info, **kwargs):
        return [leader for leader in self.gym_leaders.all()]

    def resolve_elite_four(self, info, **kwargs):
        return [elite for elite in self.elite_four.all()]

    def resolve_champion(self, info, **kwargs):
        return self.champion

    def resolve_competitors(self, info, **kwargs):
        return [trainer for trainer in self.competitors.all()]

    def resolve_winner(self, info, **kwargs):
        return self.winner

    class Meta:
        interfaces = (graphene.relay.Node,)


class LeaderType(graphene.ObjectType):
    """
    Defines a GraphQL  serializer object for the Leader Model.
    """
    name = graphene.String()
    role = Role()
    pokemon_type = PokemonTypes()
    clauses = graphene.String()
    join_date = graphene.DateTime()
    battle_counter = graphene.Int()
    win_percentage = graphene.Float()
    loose_percentage = graphene.Float()
    lv = graphene.Int()
    next_lv = graphene.Int()
    fc = graphene.String()
    sd_id = graphene.String()
    exp = graphene.Int()
    discord_id = graphene.String()

    class Meta:
        interfaces = (graphene.relay.Node,)


class TrainerType(graphene.ObjectType):
    """
    Defines a GraphQL serializer object for the Trainer Model
    """
    name = graphene.String()
    join_date = graphene.DateTime()
    battle_counter = graphene.Int()
    badge_counter = graphene.Int()
    leagues_counter = graphene.Int()
    win_percentage = graphene.Float()
    loose_percentage = graphene.Float()
    leagues = graphene.relay.ConnectionField('abp.schema.LeagueConnection')
    scores = graphene.relay.ConnectionField('abp.schema.ScoreConnection')
    lv = graphene.Int()
    next_lv = graphene.Int()
    fc = graphene.String()
    sd_id = graphene.String()
    exp = graphene.Int()
    discord_id = graphene.String()

    def resolve_scores(self, info, **kwargs):
        return [score for score in self.score_set.all()]

    def resolve_leagues(self, info, **kwargs):
        return [league for league in self.league_competitors.all()]

    class Meta:
        interfaces = (graphene.relay.Node,)


class ScoreType(graphene.ObjectType):
    """
    Defines a GraphQL serializer object for the score model
    """
    league = graphene.Field(LeagueType)
    trainer = graphene.Field(TrainerType)
    wins = graphene.Int()
    losses = graphene.Int()
    battles = graphene.relay.ConnectionField('abp.schema.BattleConnection')
    badges = graphene.List(graphene.String)

    def resolve_league(self, info, **kwargs):
        return self.league

    def resolve_trainer(self, info, **kwargs):
        return self.trainer

    def resolve_battles(self, info, **kwargs):
        return self.battles.all()

    def resolve_badges(self, info, **kwargs):
        return [badge.reference for badge in self.badges.all()]

    class Meta:
        interfaces = (graphene.relay.Node,)


class BattleType(graphene.ObjectType):
    """
    Defines a GraphQL serializer object for the battle models.
    """
    battle_datetime = graphene.DateTime()
    winner = graphene.String()
    trainer = graphene.Field(TrainerType)
    leader = graphene.Field(LeaderType)

    def resolve_winner(self, info, **kwargs):
        return self.winner_name

    def resolve_trainer(self, info, **kwargs):
        return self.trainer

    def resolve_leader(self, info, **kwargs):
        return self.leader

    class Meta:
        interfaces = (graphene.relay.Node,)


#######################################################
#                  Relay Connections
#######################################################
class LeagueConnection(graphene.relay.Connection):
    class Meta:
        node = LeagueType


class TrainerConnection(graphene.relay.Connection):
    class Meta:
        node = TrainerType


class LeaderConnection(graphene.relay.Connection):
    class Meta:
        node = LeaderType


class ScoreConnection(graphene.relay.Connection):
    class Meta:
        node = ScoreType


class BattleConnection(graphene.relay.Connection):
    class Meta:
        node = BattleType


#######################################################
#                  GraphQL Query
#######################################################
class Query(object):
    """
    ABP Queries
    """
    node = graphene.relay.Node.Field()

    ###################################################
    #                       Leagues
    ###################################################
    leagues = graphene.relay.ConnectionField(
        LeagueConnection,
        id=graphene.ID(
            description='Filters league by ID.'
        ),
        reference__icontains=graphene.String(
            description='Filters league which referece contains the give value'
        ),
    )
    def resolve_leagues(self, info, **kwargs):
        return resolve_leagues(**kwargs)

    ###################################################
    #                       Trainers
    ###################################################
    trainers = graphene.relay.ConnectionField(
        TrainerConnection,
        id=graphene.ID(description='Filters by trainer ID.'),
        name__icontains=graphene.String(
            description='Filters by trainer name containing the given string.'
        ),
        battle_counter__gte=graphene.Int(
            description='Trainers battle counter greater equal the given value.'
        ),
        battle_counter__lte=graphene.Int(
            description='Trainers battle counter less equal the given value.'
        ),
        badge_counter__gte=graphene.Int(
            description='Trainers badge counter greater equal the given value.'
        ),
        badge_counter__lte=graphene.Int(
            description='Trainers badge counter less equal the given value.'
        ),
        leagues_counter__gte=graphene.Int(
            description='Trainers league counter greater equal the given value.'
        ),
        leagues_counter__lte=graphene.Int(
            description='Trainers league counter less equal the given value.'
        ),
        win_percentage__gte=graphene.Float(
            description='Trainers win percentage greater equal the given value.'
        ),
        win_percentage__lte=graphene.Float(
            description='Trainers win percentage less equal the given value.'
        ),
        loose_percentage__gte=graphene.Float(
            description='Trainers loose percentage greater equal the given value.'
        ),
        loose_percentage__lte=graphene.Float(
            description='Trainers loose percentage less equal the given value.'
        ),
        discord_id__icontains=graphene.String(
            description='Trainer by discord user ID'
        ),
    )
    def resolve_trainers(self, info, **kwargs):
        return resolve_trainers(**kwargs)

    ###################################################
    #                       Leaders
    ###################################################
    leaders = graphene.relay.ConnectionField(
        LeaderConnection,
        id=graphene.ID(description='Filters by leader ID.'),
        name__icontains=graphene.String(
            description='Filters by leader name containing the given string.'
        ),
        battle_counter__gte=graphene.Int(
            description='Leaders battle counter greater equal the given value.'
        ),
        battle_counter__lte=graphene.Int(
            description='Leaders battle counter less equal the given value.'
        ),
        win_percentage__gte=graphene.Float(
            description='Leaders win percentage greater equal the given value.'
        ),
        win_percentage__lte=graphene.Float(
            description='Leaders win percentage less equal the given value.'
        ),
        loose_percentage__gte=graphene.Float(
            description='Leaders loose percentage greater equal the given value.'
        ),
        loose_percentage__lte=graphene.Float(
            description='Leaders loose percentage less equal the given value.'
        ),
    )
    def resolve_leaders(self, info, **kwargs):
        return resolve_leaders(**kwargs)

    ###################################################
    #                       Scores
    ###################################################
    scores = graphene.relay.ConnectionField(
        ScoreConnection,
        league__id__in=graphene.List(
            graphene.ID,
            description='Scores from the given leagues.'
        ),
        trainer__id__in=graphene.List(
            graphene.ID,
            description='Scores from the given trainers.'
        )
    )
    def resolve_scores(self, info, **kwargs):
        return resolve_scores(**kwargs)

    ###################################################
    #                       Battles
    ###################################################
    battles = graphene.relay.ConnectionField(
        BattleConnection,
        trainer__id__in=graphene.List(
            graphene.ID,
            description='Battles from given trainer'
        ),
        leader__id__in=graphene.List(
            graphene.ID,
            description='Battles from given leader'
        )
    )
    def resolve_battles(self, info, **kwargs):
        return resolve_battles(**kwargs)

    ###################################################
    #                       Badges
    ###################################################
    badges = graphene.String()
    def resolve_badges(self, info, **kwargs):
        return [badge.reference for badge in Badge.objects.all()]


#######################################################
#                  Create Mutations
#######################################################
class CreateLeague(graphene.relay.ClientIDMutation):
    """
    Creates a league.
    """
    league = graphene.Field(
        LeagueType
    )

    class Input:
        reference = graphene.String(required=True)
        start_date = graphene.Date(required=False)
        end_date = graphene.Date(required=False)
        description = graphene.String(required=False)

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description', '')

        try:
            league = League.objects.create(
                reference=reference,
                start_date=start_date,
                end_date=end_date,
                description=description,
            )
        except Exception as ex:
            raise Exception(ex)

        league.save()
        return CreateLeague(league)


class CreateTrainer(graphene.relay.ClientIDMutation):
    """
    Creates a trainer.
    """
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        discord_id = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        discord_id = _input.get('discord_id')

        try:
            trainer = Trainer.objects.create(
                discord_id=discord_id
            )
        except Exception as ex:
            raise Exception(ex)

        trainer.save()
        return CreateTrainer(trainer)


class CreateLeader(graphene.relay.ClientIDMutation):
    """
    Creates a leader.
    """
    leader = graphene.Field(
        LeaderType
    )

    class Input:
        discord_id = graphene.String(required=True)
        pokemon_type = PokemonTypes(required=True)
        role = Role(required=True)

    def mutate_and_get_payload(self, info, **_input):
        discord_id = _input.get('discord_id')
        pokemon_type = _input.get('pokemon_type')
        role = _input.get('role')

        try:
            leader = Leader.objects.create(
                discord_id=discord_id,
                pokemon_type=pokemon_type,
                role=role
            )
        except Exception as ex:
            raise Exception(ex)

        leader.save()
        return CreateLeader(leader)


#######################################################
#                  Update Mutations
#######################################################
class UpdateLeague(graphene.relay.ClientIDMutation):
    """
    Updates a league.
    """
    league = graphene.Field(
        LeagueType
    )

    class Input:
        reference = graphene.String(required=False)
        start_date = graphene.Date(required=False)
        end_date = graphene.Date(required=False)
        description = graphene.String(required=False)
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference', '')
        start_date = _input.get('start_date', '')
        end_date = _input.get('end_date', '')
        description = _input.get('description', '')
        global_id = _input.get('id')

        kind, league_id = from_global_id(global_id)

        # Verifica que o id é de uma League
        if not kind == 'LeagueType':
            raise Exception(
                'The ID doesnt match with a League object!'
            )

        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception(
                'Sorry, the given League does not exist!'
            )

        if reference:
            league.reference = reference
        if start_date:
            league.start_date = start_date
        if end_date:
            league.end_date = end_date
        if description:
            league.description = description
        league.save()

        return UpdateLeague(league)


class UpdateTrainer(graphene.relay.ClientIDMutation):
    """
    Updates a trainer.
    """
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        name = graphene.String()

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        name = _input.get('name')

        kind, trainer_id = from_global_id(global_id)

        # Check if is the right ID
        if not kind == 'TrainerType':
            raise Exception(
                'Wrong Trainer ID.'
            )

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Exception(
                'Sorry, the given trainer does not exist!'
            )

        if name:
            trainer.nickname = nickname
        trainer.save()
        return UpdateTrainer(trainer)


class UpdateLeader(graphene.relay.ClientIDMutation):
    """
    Updates a leader.
    """
    leader = graphene.Field(
        LeaderType
    )

    class Input:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        pokemon_type = PokemonTypes(required=False)
        role = Role(required=False)

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        name = _input.get('name', '')
        pokemon_type = _input.get('pokemon_type', '')
        role = _input.get('role', '')

        kind, leader_id = from_global_id(global_id)
        if not kind == 'LeaderType':
            raise Exception('Wrong leader ID.')

        try:
            leader = Leader.objects.get(id=leader_id)
        except Leader.DoesNotExist:
            raise Exception('Sorry, this leader does not exist.')

        if name:
            leader.nickname = nickname
        if pokemon_type:
            leader.pokemon_type = pokemon_type
        if role:
            leader.role = role
        leader.save()
        return UpdateLeader(leader)


#######################################################
#                  Delete Mutations
#######################################################
class DeleteLeague(graphene.relay.ClientIDMutation):
    """
    Deletes a league.
    """
    league = graphene.Field(
        LeagueType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id', '')
        kind, league_id = from_global_id(global_id)

        # Verifica que o id é de uma League
        if not kind == 'LeagueType':
            raise Exception(
                'The ID doesnt match with a League object!'
            )

        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception(
                'Sorry, the given League does not exist!'
            )

        league.delete()

        return DeleteLeague(league)


class DeleteTrainer(graphene.relay.ClientIDMutation):
    """
    Deletes a trainer.
    """
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id', '')
        kind, trainer_id = from_global_id(global_id)

        # Check if is the right ID
        if not kind == 'TrainerType':
            raise Exception(
                'Wrong Trainer ID.'
            )

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Exception(
                'Sorry, the given trainer does not exist!'
            )

        trainer.delete()
        return DeleteTrainer(trainer)


class DeleteLeader(graphene.relay.ClientIDMutation):
    """
    Deletes a leader.
    """
    leader = graphene.Field(
        LeaderType
    )

    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')

        kind, leader_id = from_global_id(global_id)
        if not kind == 'LeaderType':
            raise Exception('Wrong leader ID.')

        try:
            leader = Leader.objects.get(id=leader_id)
        except Leader.DoesNotExist:
            raise Exception('Sorry, this leader does not exist.')

        leader.delete()
        return DeleteLeader(leader)


#######################################################
#                  Other Mutations
#######################################################
class LeagueRegistration(graphene.relay.ClientIDMutation):
    """
    Register a trainer into a league.
    """
    registration = graphene.String()

    class Input:
        discord_id = graphene.ID(
            required=True
        )
        league = graphene.ID(
            required=True
        )
        is_trainer = graphene.Boolean(required=True)

    def mutate_and_get_payload(self, info, **_input):
        discord_id = _input.get('discord_id')
        league_global_id = _input.get('league')
        is_trainer = _input.get('is_trainer')

        kind, league_id = from_global_id(league_global_id)
        if not kind == 'LeagueType':
            raise Exception(
                'Wrong League ID was given.'
            )

        # Verifica se a liga existe
        # TODO verificar se a liga ja nao foi encerrada
        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception(
                'Sorry, this league does not exist.'
            )

        if is_trainer:
            try:
                trainer = Trainer.objects.get(discord_id=discord_id)
            except Trainer.DoesNotExist:
                raise Exception(
                    'Sorry, this trainer does not exist.'
                )

            # se o jogador ja estiver registrado nesta liga
            if trainer in league.competitors.all():
                raise Exception(
                    'This trainer is already registered in this league'
                )
            league.competitors.add(trainer)
            league.save()
            trainer.leagues_counter += 1
            trainer.save()

            # Cria um score do treinador para esta liga
            score = Score.objects.create(
                trainer=trainer,
                league=league
            )
            score.save()

        else:
            # Verifica se o lider existe no banco de dados
            try:
                leader = Leader.objects.get(discord_id=discord_id)
            except Leader.DoesNotExist:
                raise Exception(
                    'Sorry, this leader does not exist.'
                )

            # verifica se o lider ja esta registrado nesta liga
            if leader in league.gym_leaders.all() or \
                leader in league.elite_four.all() or \
                leader == league.champion:
                raise Exception(
                    'This leader is already registered in this league!'
                )

            # verifica para qual função o líder foi designado
            if leader.role == 'Gym Leader':
                league.gym_leaders.add(leader)

            elif leader.role == 'Elite Four':
                if not len(league.elite_four.all()) < 4:
                    raise Exception('The league elite four is already fullfilled')
                league.elite_four.add(leader)

            elif leader.role == 'Champion':
                if not league.champion:
                    league.champion = leader
                else:
                    raise Exception(
                        'This league champion has already been registered'
                    )
            else:
                raise Exception(
                    'This leader has no role yet. Please give him a role before' \
                    'registering at this league!'
                )

        return LeagueRegistration(
            f'registration at {league.reference} complete!'
        )


class BattleRegister(graphene.relay.ClientIDMutation):
    """
    Register a battle between a trainer and a leader.
    """
    battle = graphene.Field(BattleType)

    class Input:
        league = graphene.ID(required=True)
        trainer = graphene.String(required=True)
        leader = graphene.String(required=True)
        winner = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        league_global_id = _input.get('league')
        trainer_discord = _input.get('trainer')
        leader_discord = _input.get('leader')
        winner = _input.get('winner')

        # Verifica a liga fornecida
        kind, league_id = from_global_id(league_global_id)
        if not kind == 'LeagueType':
            raise Exception('Wrong league ID.')

        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception('Sorry, this league does not exist.')

        # Tenta recupera o treiandor
        try:
            trainer = Trainer.objects.get(discord_id=trainer_discord)
        except Trainer.DoesNotExist:
            raise Exception('Trainer was not found on database!')

        # Tenta recupera o líder
        try:
            leader = Leader.objects.get(discord_id=leader_discord)
        except Leader.DoesNotExist:
            raise Exception('Trainer not found on database!')

        # Recupera o score do treinador
        try:
            trainer_score = trainer.score_set.get(league=league)
        except Score.DoesNotExist:
            raise Exception(
                'This trainer doesnt seems to be registered ' \
                'on the given league!'
            )

        # Verifica que o vencedor é um dos dois fornecidos
        if not winner == trainer.discord_id and not winner == leader.discord_id:
            raise Exception('The winner must be the given leader or trainer.')

        # Registra a batalha
        battle = Battle.objects.create(
            leader=leader,
            trainer=trainer,
            winner_name=winner
        )
        battle.save()

        # Relaciona a batalha criada ao score do treinador
        trainer_score.battles.add(battle)

        # incrementa o contrador de batalhas dos lutadores
        trainer.battle_counter += 1
        leader.battle_counter += 1

        # calcula o total de experência que a batalha fornecerá
        exp = get_exp(trainer.lv, leader.lv)

        # Se o vencedor for o treinador
        if winner == trainer_discord:
            # Atualiza os stats dos lutadores e do score
            trainer.total_wins += 1
            trainer_score.wins += 1
            leader.total_losses += 1

            # Adiciona experiência e recalcula o Lv
            trainer.exp += exp
            leader.exp += ceil(exp/4)
            lv_update(trainer)
            lv_update(leader)

        # Se o vencedor for o lider
        else:
            # Atualiza os stats dos lutadores e do score
            trainer.total_losses += 1
            trainer_score.losses += 1
            leader.total_wins += 1

            # Adiciona experiência e recalcula o Lv
            trainer.exp += ceil(exp/4)
            leader.exp += exp
            lv_update(trainer)
            lv_update(leader)

        # Atualiza a porcentagem de vitorias/derrotas dos lutadores
        trainer.win_percentage = (trainer.total_wins / trainer.battle_counter) * 100
        trainer.loose_percentage = (trainer.total_losses / trainer.battle_counter) * 100
        leader.win_percentage = (leader.total_wins / leader.battle_counter) * 100
        leader.loose_percentage = (leader.total_losses / leader.battle_counter) * 100

        trainer.save()
        leader.save()
        trainer_score.save()

        return BattleRegister(battle)


class AddBadgeToTrainer(graphene.relay.ClientIDMutation):
    """
    Gives a badge do a trainer.
    """
    response = graphene.String()

    class Input:
        trainer_name = graphene.String(required=True)
        badge = graphene.String(required=True)
        league = graphene.ID(required=True)

    def mutate_and_get_payload(self, info, **_input):
        trainer_name = _input.get('trainer_name')
        badge_reference = _input.get('badge').title()
        league_global_id = _input.get('league')

        # Verifica a liga fornecida
        kind, league_id = from_global_id(league_global_id)
        if not kind == 'LeagueType':
            raise Exception('Wrong league ID.')
        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception('Sorry, this league does not exist.')

        # Tenta recuperar a insígnia do banco de dados
        try:
            badge = Badge.objects.get(reference=badge_reference)
        except Badge.DoesNotExist:
            raise Exception('This Badge does not exist!')

        # Tenta recuperar o treinador
        try:
            trainer = Trainer.objects.get(name=trainer_name)
        except Trainer.DoesNotExist:
            raise Exception(f'The trainer {trainer_name} does not exist')

        # Recupera o score do treinador
        try:
            trainer_score = trainer.score_set.get(league=league)
        except Score.DoesNotExist:
            raise Exception(
                'This trainer doesnt seems to be registered ' \
                'on the given league!'
            )

        # verifica que o treinaro ainda não possui esta insígina
        if badge in trainer_score.badges.all():
            raise Exception('This trainer already have this badge!')

        # Adiciona a insígnia ao treinador
        trainer_score.badges.add(badge)
        trainer.badge_counter += 1

        trainer_score.save()
        trainer.save()

        return AddBadgeToTrainer(
            f'{trainer_name} received {badge_reference} badge!'
        )


class AutoCreateBadges(graphene.relay.ClientIDMutation):
    """
    Auto creates all badge types.
    """
    response = graphene.List(graphene.String)

    def mutate_and_get_payload(self, info, **kwargs):
        badge_types = (
            'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting',
            'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost',
            'Dark', 'Dragon', 'Steel', 'Fairy'
        )
        badges_created = []
        for badge in badge_types:
            try:
                bdg = Badge.objects.create(reference=badge)
                badges_created.append(badge)
                bdg.save()
            except:
                pass

        return AutoCreateBadges(badges_created)


#######################################################
#                  Main Mutation
#######################################################
class Mutation:
    # Create
    create_league = CreateLeague.Field()
    create_trainer = CreateTrainer.Field()
    create_leader = CreateLeader.Field()

    # Update
    update_league = UpdateLeague.Field()
    update_trainer = UpdateTrainer.Field()
    update_leader = UpdateLeader.Field()

    # Delete
    delete_league = DeleteLeague.Field()
    delete_trainer = DeleteTrainer.Field()
    delete_leader = DeleteLeader.Field()

    # Other
    league_registration = LeagueRegistration.Field()
    battle_register = BattleRegister.Field()
    add_badge_to_trainer = AddBadgeToTrainer.Field()
    auto_create_badges = AutoCreateBadges.Field()
