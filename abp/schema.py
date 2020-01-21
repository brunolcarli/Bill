import graphene
from abp.models import (Battle, League, Trainer, Score, Leader)
from graphql_relay import from_global_id



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
    # scores

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
    # TODO link to scores

    def resolve_leagues(self, info, **kwargs):
        return [league for league in self.league_competitors.all()]

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
        LeagueConnection
    )
    def resolve_leagues(self, info, **kwargs):
        return League.objects.all()

    ###################################################
    #                       Trainers
    ###################################################
    trainers = graphene.relay.ConnectionField(
        TrainerConnection
    )
    def resolve_trainers(self, info, **kwargs):
        return Trainer.objects.all()

    ###################################################
    #                       Leaders
    ###################################################
    leaders = graphene.relay.ConnectionField(
        LeaderConnection
    )
    def resolve_leaders(self, info, **kwargs):
        return Leader.objects.all()

    ###################################################
    #                       Scores
    ###################################################
    # TODO

    ###################################################
    #                       Battles
    ###################################################
    # TODO


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
        name = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        name = _input.get('name')

        try:
            trainer = Trainer.objects.create(
                name=name
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
        name = graphene.String(required=True)
        pokemon_type = PokemonTypes(required=True)
        role = Role(required=True)

    def mutate_and_get_payload(self, info, **_input):
        nickname = _input.get('nickname')
        pokemon_type = _input.get('pokemon_type')
        role = _input.get('role')

        try:
            leader = Leader.objects.create(
                name=name,
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
        trainer = graphene.ID(
            required=True
        )
        league = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        trainer_global_id = _input.get('trainer')
        league_global_id = _input.get('league')

        kind, trainer_id = from_global_id(trainer_global_id)
        if not kind == 'TrainerType':
            raise Exception(
                'Wrong Trainer ID was given.'
            )

        kind, league_id = from_global_id(league_global_id)
        if not kind == 'LeagueType':
            raise Exception(
                'Wrong League ID was given.'
            )

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Exception(
                'Sorry, this trainer does not exist.'
            )

        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Exception(
                'Sorry, this league does not exist.'
            )

        if trainer in league.competitors.all():
            raise Exception('This trainer is already registered in this league')

        # TODO verificar se a liga ja nao foi encerrada
        league.competitors.add(trainer)
        league.save()

        trainer.leagues_counter += 1
        trainer.save()

        # TODO criar um score linkando este trainer com esta liga

        return LeagueRegistration(
            f'{trainer.name} registration at {league.reference} complete!'
        )


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
