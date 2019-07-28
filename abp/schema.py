import graphene
from abp.models import (Season, Tournament, League, Trainer, LeagueScore,
                        TournamentScore)
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

    league = graphene.Field(
        'abp.schema.LeagueType'
    )

    def resolve_tournaments(self, info, **kwargs):
        return self.tournament_set.all()

    def resolve_league(self, info, **kwargs):
        return next(iter(self.league_set.all()))


class TournamentType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()
    registered_trainers = graphene.ConnectionField(
        'abp.schema.TrainerConnection'
    )

    # TODO link to season

    def resolve_registered_trainers(self, info, **kwargs):
        return [t.trainer_reference for t in self.tournamentscore_set.all()]


class LeagueType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    # TODO: Think a way to inherit repeated fields from another generic class
    reference = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()
    
    registered_trainers = graphene.relay.ConnectionField(
        'abp.schema.TrainerConnection'
    )

    def resolve_registered_trainers(self, info, **kwargs):
        return [t.trainer_reference for t in self.leaguescore_set.all()]


# TODO class LeaderType


class LeagueScoreType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    league = graphene.Field(
        'abp.schema.LeagueType'
    )
    trainer = graphene.Field(
        'abp.schema.TrainerType'
    )

    def resolve_league(self, info, **kwargs):
        return self.league_reference

    def resolve_trainer(self, info, **kwargs):
        return self.trainer_reference


class TournamentScoreType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    tournament = graphene.Field(
        'abp.schema.TournamentType'
    )
    trainer = graphene.Field(
        'abp.schema.TrainerType'
    )

    def resolve_tournament(self, info, **kwargs):
        return self.tournament_reference

    def resolve_trainer(self, info, **kwargs):
        return self.trainer_reference


class TrainerGlobalStatus(graphene.ObjectType):
    num_wins = graphene.Int()
    num_losses = graphene.Int()
    num_battles = graphene.Int()


class TrainerType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    nickname = graphene.String()
    registration_datetime = graphene.DateTime()
    tournament_scores = graphene.relay.ConnectionField(
        'abp.schema.TournamentScoreConnection'
    )
    global_status = graphene.Field(
        TrainerGlobalStatus
    )

    def resolve_registration_datetime(self, info, **kwargs):
        return self.registration_date

    def resolve_tournament_scores(self, info, **kwargs):
        return self.tournamentscore_set.all()

    def resolve_global_status(self, info, **kwargs):
        status = TrainerGlobalStatus(
            num_wins=self.num_wins,
            num_losses=self.num_losses,
            num_battles=self.num_battles
        )
        return status

    # TODO link to league scores
    # TODO link to battles


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


class TrainerConnection(graphene.relay.Connection):
    class Meta:
        node = TrainerType


class TournamentScoreConnection(graphene.relay.Connection):
    class Meta:
        node = TournamentScoreType


class LeagueScoreConnection(graphene.relay.Connection):
    class Meta:
        node = LeagueScoreType


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

    ###################################################
    #                       Trainers
    ###################################################
    trainers = graphene.relay.ConnectionField(
        TrainerConnection
    )
    def resolve_trainers(self, info, **kwargs):
        return Trainer.objects.all()

    ###################################################
    #                       Scores
    ###################################################
    tournament_scores = graphene.relay.ConnectionField(
        TournamentScoreConnection
    )
    def resolve_tournament_scores(self, info, **kwargs):
        return TournamentScore.objects.all()

    league_scores = graphene.ConnectionField(
        LeagueScoreConnection
    )
    def resolve_league_scores(self, info, **kwargs):
        return LeagueScore.objects.all()


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


class CreateTrainer(graphene.relay.ClientIDMutation):
    '''
        Creates a trainer.
    '''
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        nickname = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        nickname = _input.get('nickname')

        try:
            trainer = Trainer.objects.create(
                nickname=nickname
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            trainer.save()
            return CreateTrainer(trainer)


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


class UpdateTrainer(graphene.relay.ClientIDMutation):
    '''
        Updates a trainer.
    '''
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        nickname = graphene.String()

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
        nickname = _input.get('nickname')

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
        else:
            if nickname:
                trainer.nickname = nickname
            trainer.save()
            return UpdateTrainer(trainer)


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


class DeleteTrainer(graphene.relay.ClientIDMutation):
    '''
        Deletes a trainer.
    '''
    trainer = graphene.Field(
        TrainerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        global_id = _input.get('id')
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
        else:
            trainer.delete()
            return DeleteTrainer(trainer)


#######################################################
#                  Other Mutations
#######################################################
class TournamentRegistration(graphene.relay.ClientIDMutation):
    '''
        Register a trainer into a tournament.
    '''
    tournament_score = graphene.Field(
        TournamentScoreType
    )

    class Input:
        trainer = graphene.ID(
            required=True
        )
        tournament = graphene.ID(
            required=True
        )

    def mutate_and_get_payload(self, info, **_input):
        trainer_global_id = _input.get('trainer')
        tournament_global_id = _input.get('tournament')

        kind, trainer_id = from_global_id(trainer_global_id)
        if not kind == 'TrainerType':
            raise Exception(
                'Wrong Trainer ID was given.'
            )

        kind, tournament_id = from_global_id(tournament_global_id)
        if not kind == 'TournamentType':
            raise Exception(
                'Wrong Tournament ID was given.'
            )

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Exception(
                'Sorry, this trainer does not exist.'
            )

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            raise Exception(
                'Sorry, this tournament does not exist.'
            )

        # TODO verificar se o torneio ja nao foi encerrado

        reference = '{} registration at {}'.format(
            trainer.nickname,
            tournament.name
        )

        try:
            score = TournamentScore.objects.create(
                reference=reference,
                tournament_reference=tournament,
                trainer_reference=trainer
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            score.save()
            return TournamentRegistration(score)


class LeagueRegistration(graphene.relay.ClientIDMutation):
    '''
        Register a trainer into a league.
    '''
    league_score = graphene.Field(
        LeagueScoreType
    )

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

        # TODO verificar se a liga ja nao foi encerrada

        reference = '{} registration at {}'.format(
            trainer.nickname,
            league.reference
        )

        try:
            score = LeagueScore.objects.create(
                reference=reference,
                league_reference=league,
                trainer_reference=trainer
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            score.save()
            return LeagueRegistration(score)


#######################################################
#                  Main Mutation
#######################################################
class Mutation:
    # Create
    create_season = CreateSeason.Field()
    create_tournament = CreateTournament.Field()
    create_league = CreateLeague.Field()
    create_trainer = CreateTrainer.Field()

    # Update
    update_season = UpdateSeason.Field()
    update_tournament = UpdateTournament.Field()
    update_league = UpdateLeague.Field()
    update_trainer = UpdateTrainer.Field()

    # Delete
    delete_season = DeleteSeason.Field()
    delete_tournament = DeleteTournament.Field()
    delete_league = DeleteLeague.Field()
    delete_trainer = DeleteTrainer.Field()

    # Other
    tournament_registration = TournamentRegistration.Field()
    league_registration = LeagueRegistration.Field()
