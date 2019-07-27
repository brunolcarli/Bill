import graphene
from abp.models import Season, Tournament, League
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

    tournaments = graphene.relay.ConnectionField(
        'abp.schema.TournamentConnection'
    )

    # TODO add league

    def resolve_tournaments(self, info, **kwargs):
        return self.tournament_set.all()


class TournamentType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()

    # TODO link to season
    # TODO link to trainers


class LeagueType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    # TODO: Think a way to inherit repeated fields from another generic class
    reference = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()


#######################################################
#                  Relay Connections
#######################################################
class SeasonlConnection(graphene.relay.Connection):
    class Meta:
        node = SeasonType


class TournamentConnection(graphene.relay.Connection):
    class Meta:
        node = TournamentType


class LeagueConnection(graphene.relay.Connection):
    class Meta:
        node = LeagueType


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

    ###################################################
    #                       Tournaments
    ###################################################
    tournaments = graphene.relay.ConnectionField(
        TournamentConnection
    )
    def resolve_tournaments(self, info, **kwargs):
        return Tournament.objects.all()

    ###################################################
    #                       Leagues
    ###################################################
    leagues = graphene.relay.ConnectionField(
        LeagueConnection
    )
    def resolve_leagues(self, info, **kwargs):
        return League.objects.all()


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


class CreateTournament(graphene.relay.ClientIDMutation):
    '''
        Creates a tournament
    '''
    tournament = graphene.Field(
        TournamentType
    )

    class Input:
        name = graphene.String(
            required=True
        )
        start_date = graphene.Date()
        end_date = graphene.Date()
        description = graphene.String()
        season_id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        name = _input.get('name')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description', '')
        season_global_id = _input.get('season_id')

        kind, season_id = from_global_id(season_global_id)

        # Verifica que o id é de uma Season
        if not kind == 'SeasonType':
            raise Exception(
                'The ID doesnt match with a Season object!'
            )

        try:
            tournament_season = Season.objects.get(id=season_id)
        except Season.DoesNotExist:
            raise Exception(
                'Sorry, the given Season does not exist!'
            )

        try:
            tournament = Tournament.objects.create(
                name=name,
                start_date=start_date,
                end_date=end_date,
                description=description,
                tournament_season=tournament_season
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            tournament.save()
            return CreateTournament(tournament)


class CreateLeague(graphene.relay.ClientIDMutation):
    '''
        Creates a league.
    '''
    league = graphene.Field(
        LeagueType
    )

    class Input:
        reference = graphene.String(required=True)
        start_date = graphene.Date()
        end_date = graphene.Date()
        description = graphene.String()
        season_id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description', '')
        season_global_id = _input.get('season_id')

        kind, season_id = from_global_id(season_global_id)

        # Verifica que o id é de uma Season
        if not kind == 'SeasonType':
            raise Exception(
                'The ID doesnt match with a Season object!'
            )

        try:
            league_season = Season.objects.get(id=season_id)
        except Season.DoesNotExist:
            raise Exception(
                'Sorry, the given Season does not exist!'
            )

        try:
            league = League.objects.create(
                reference=reference,
                start_date=start_date,
                end_date=end_date,
                description=description,
                league_season=league_season
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            league.save()
            return CreateLeague(league)


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


class UpdateTournament(graphene.relay.ClientIDMutation):
    '''
        Updates a tournament
    '''
    tournament = graphene.Field(
        TournamentType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        name = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        description = graphene.String()

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        name = _input.get('name')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
        description = _input.get('description')

        kind, tournament_id = from_global_id(global_id)

        # Verifica que o id é de um Tournament
        if not kind == 'TournamentType':
            raise Exception(
                'The ID doesnt match with a Tournament object!'
            )

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            raise Exception(
                'Sorry, the given Tournament does not exist!'
            )

        else:
            if name:
                tournament.name = name
            if start_date:
                tournament.start_date = start_date
            if end_date:
                tournament.end_date = end_date
            if description:
                tournament.description = description
            tournament.save()

            return UpdateTournament(tournament)


class UpdateLeague(graphene.relay.ClientIDMutation):
    '''
        Updates a league.
    '''
    league = graphene.Field(
        LeagueType
    )

    class Input:
        reference = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        description = graphene.String()
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        start_date = _input.get('start_date')
        end_date = _input.get('end_date')
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
        else:
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


class DeleteTournament(graphene.relay.ClientIDMutation):
    '''
        Deletes a tournament
    '''
    tournament = graphene.Field(
        TournamentType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        kind, tournament_id = from_global_id(global_id)

        # Verifica que o id é de um Tournament
        if not kind == 'TournamentType':
            raise Exception(
                'The ID doesnt match with a Tournament object!'
            )

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            raise Exception(
                'Sorry, the given Tournament does not exist!'
            )

        else:
            tournament.delete()
            return DeleteTournament(tournament)


class DeleteLeague(graphene.relay.ClientIDMutation):
    '''
        Deletes a league.
    '''
    league = graphene.Field(
        LeagueType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
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
        else:
            league.delete()

            return DeleteLeague(league)


#######################################################
#                  Main Mutation
#######################################################
class Mutation:
    # Create
    create_season = CreateSeason.Field()
    create_tournament = CreateTournament.Field()
    create_league = CreateLeague.Field()

    # Update
    update_season = UpdateSeason.Field()
    update_tournament = UpdateTournament.Field()
    update_league = UpdateLeague.Field()

    # Delete
    delete_season = DeleteSeason.Field()
    delete_tournament = DeleteTournament.Field()
    delete_league = DeleteLeague.Field()
