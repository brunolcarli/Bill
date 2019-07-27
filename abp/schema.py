import graphene
from abp.models import Season, Tournament
from graphql_relay import from_global_id


#######################################################
#                  GraphQL Types
#######################################################
class SeasonType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()

    # TODO add tournaments
    # TODO add league


class TournamentType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()

    # TODO link to season
    # TODO link to trainers


#######################################################
#                  Relay Connections
#######################################################
class SeasonlConnection(graphene.relay.Connection):
    class Meta:
        node = SeasonType


class TournamentConnection(graphene.relay.Connection):
    class Meta:
        node = TournamentType


#######################################################
#                  GraphQL Query
#######################################################
class Query(object):
    '''
        ABP Queries
    '''
    node = graphene.relay.Node.Field()

    ###################################################
    #                       Seasons
    ###################################################
    seasons = graphene.relay.ConnectionField(
        SeasonlConnection
    )
    def resolve_seasons(self, info, **kwargs):
        return Season.objects.all()

    tournaments = graphene.relay.ConnectionField(
        TournamentConnection
    )
    def resolve_tournaments(self, info, **kwargs):
        return Tournament.objects.all()


#######################################################
#                  Create Mutations
#######################################################
class CreateSeason(graphene.relay.ClientIDMutation):
    '''
        Creates a season.
    '''
    season = graphene.Field(
        SeasonType
    )

    class Input:
        reference = graphene.String(
            required=True
        )
        start_date = graphene.Date(
            required=True
        )
        end_date = graphene.Date(
            required=True
        )
        description = graphene.String()

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description', '')

        try:
            season = Season.objects.create(
                reference=reference,
                start_date=start_date,
                end_date=end_date,
                description=description
            )
        # TODO handle the right error when the time come
        except Exception as ex:
            raise ex
    
        return CreateSeason(season)


#######################################################
#                  Update Mutations
#######################################################
class UpdateSeason(graphene.relay.ClientIDMutation):
    '''
        Updates a season information.
    '''
    season = graphene.Field(
        SeasonType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        reference = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        description = graphene.String()

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description', '')
        global_id = _input.get('id')
        _, season_id = from_global_id(global_id)    

        try:
            season = Season.objects.get(id=season_id)
        except Season.DoesNotExist:
            raise Exception(
                'Sorry, the given season does not exist!'
            )
        else:
            if reference:
                season.reference = reference
            if start_date:
                season.start_date = start_date
            if end_date:
                season.end_date = end_date
            if description:
                season.description = description
            season.save()
            return UpdateSeason(season)


#######################################################
#                  Delete Mutations
#######################################################
class DeleteSeason(graphene.relay.ClientIDMutation):
    '''
        Deletes a season.
    '''
    season = graphene.Field(
        SeasonType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        _, season_id = from_global_id(global_id)

        try:
            season = Season.objects.get(id=season_id)
        except Season.DoesNotExist:
            raise Exception(
                'Sorry, the given season does not exist!'
            )
        else:
            season.delete()
            return DeleteSeason(season)


#######################################################
#                  Main Mutation
#######################################################
class Mutation:
    # Create
    create_season = CreateSeason.Field()

    # Update
    update_season = UpdateSeason.Field()

    # Delete
    delete_season = DeleteSeason.Field()
