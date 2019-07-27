import graphene
from abp.models import (Season, Tournament, League, Trainer, Event,
                        Score, LeagueScore, TournamentScore)
from graphql_relay import from_global_id, to_global_id


#######################################################
#                  Interfaces
#######################################################
class TournamentEvent(graphene.Interface):
    tournament = graphene.Field(
        'abp.schema.TournamentType'
    )


class LeagueEvent(graphene.Interface):
    league = graphene.Field(
        'abp.schema.LeagueType'
    )


class TournamentScoreInterface(graphene.Interface):
    tournament_score = graphene.Field(
        'abp.schema.TournamentScoreType'
    )


class LeagueScoreInterface(graphene.Interface):
    league_score = graphene.Field(
        'abp.schema.LeagueScoreType'
    )


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


# TODO class LeaderType


class LeagueScoreType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    league = graphene.Field(
        'abp.schema.LeagueType'
    )

    def resolve_league(self, info, **kwargs):
        return self.league_reference


class TournamentScoreType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    tournament = graphene.Field(
        'abp.schema.TournamentType'
    )

    def resolve_tournament(self, info, **kwargs):
        return self.tournament_reference


class ScoreType(graphene.ObjectType):
    class Meta:
        interfaces = (
            graphene.relay.Node,
            LeagueScoreInterface,
            TournamentScoreInterface
        )

    event = graphene.Field(
        'abp.schema.EventType'
    )
    score_key = graphene.ID()

    def resolve_event(self, info, **kwargs):
        return self.event_reference

    def resolve_league_score(self, info, **kwargs):
        kind, score_id = from_global_id(self.score_key)
        if not kind == 'LeagueScoreType':
            return None
        else:
            try:
                league_score = LeagueScore.objects.get(id=score_id)
            except LeagueScore.DoesNotExist:
                return None
            else:
                return league_score

    def resolve_tournament_score(self, info, **kwargs):
        kind, score_id = from_global_id(self.score_key)
        if not kind == 'TournamentScoreType':
            return None
        else:
            try:
                tournament_score = TournamentScore.objects.get(id=score_id)
            except TournamentScore.DoesNotExist:
                return None
            else:
                return tournament_score


class EventType(graphene.ObjectType):
    class Meta:
        interfaces = (
            graphene.relay.Node,
            LeagueEvent,
            TournamentEvent
        )

    trainer = graphene.Field(
        'abp.schema.TrainerType'
    )
    event_key = graphene.ID()
    score_key = graphene.ID()

    def resolve_trainer(self, info, **kwargs):
        return self.trainer_reference

    def resolve_league(self, info, **kwargs):
        kind, league_id = from_global_id(self.event_key)
        if not kind == 'LeagueType':
            return None
        else:
            try:
                league = League.objects.get(id=league_id)
            except League.DoesNotExist:
                return None
            else:
                return league

    def resolve_tournament(self, info, **kwargs):
        kind, tournament_id = from_global_id(self.event_key)
        if not kind == 'TournamentType':
            return None
        else:
            try:
                tournament = Tournament.objects.get(id=tournament_id)
            except Tournament.DoesNotExist:
                return None
            else:
                return tournament


class TrainerType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    nickname = graphene.String()
    registration_datetime = graphene.DateTime()
    num_wins = graphene.Int()
    num_losses = graphene.Int()
    num_battles = graphene.Int()

    # TODO link to scores
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


class EventConnection(graphene.relay.Connection):
    class Meta:
        node = EventType


class ScoreConnection(graphene.relay.Connection):
    class Meta:
        node = ScoreType


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
    #                       Events
    ###################################################
    events = graphene.relay.ConnectionField(
        EventConnection
    )
    def resolve_events(self, info, **kwargs):
        return Event.objects.all()

    ###################################################
    #                       Scores
    ###################################################
    scores = graphene.relay.ConnectionField(
        ScoreConnection
    )
    def resolve_scores(self, info, **kwargs):
        return Score.objects.all()


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


class CreateEvent(graphene.relay.ClientIDMutation):
    event = graphene.Field(
        EventType
    )

    class Input:
        trainer = graphene.ID(required=True)
        event_key = graphene.ID(required=True)

    def mutate_and_get_payload(self, info, **_input):
        trainer_global_id = _input.get('trainer')
        event_global_id = _input.get('event_key')

        kind, trainer_id = from_global_id(trainer_global_id)
        # Verifica que o trainer_id é de um Trainer
        if not kind == 'TrainerType':
            raise Exception(
                'The trainer ID dont match with a Trainer object!'
            )

        try:
            trainer_reference = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Exception(
                'Sorry, the given Trainer does not exist!'
            )

        kind, event_id = from_global_id(event_global_id)
        # Verifica qual tipo de evento foi fornecido
        if kind == 'LeagueType': 
            try:
                league = League.objects.get(id=event_id)
            except League.DoesNotExist:
                raise Exception(
                    'Sorry, the given League does not exist!'
                )
            else:
                try:
                    league_score = LeagueScore.objects.create(
                        league_reference=league,
                        reference='{} {} Scoreboard'.format(
                            trainer_reference.nickname,
                            league.reference
                        )
                    )
                except Exception as ex:
                    raise Exception(ex)
                league_score.save()
                score_key = to_global_id('LeagueScoreType', league_score.id)
        
        elif kind == 'TournamentType':
            try:
                tournament = Tournament.objects.get(id=event_id)
            except Tournament.DoesNotExist:
                raise Exception(
                    'Sorry, the given Tournament does not exist!'
                )
            else:
                try:
                    tournament_score = TournamentScore.objects.create(
                        tournament_reference=tournament,
                        reference='{} {} Scoreboard'.format(
                            trainer_reference.nickname,
                            tournament.name
                        )
                    )
                except Exception as ex:
                    raise Exception(ex)
                tournament_score.save()
                score_key = to_global_id(
                    'TournamentScoreType',
                    tournament_score.id
                )
        else:
            raise Exception(
                'The given event is not valid.'
            )

        try:
            event = Event.objects.create(
                trainer_reference=trainer_reference,
                event_key=event_global_id,
                score_key='score_key'
            )
        except Exception as ex:
            raise Exception(ex)

        else:
            event.save()
            try:
                score = Score.objects.create(
                    score_key=score_key,
                    event_reference=event
                )
            except Exception as ex:
                raise Exception(ex)
            score.save()
            score_key = to_global_id(
                'ScoreType',
                score.id
            )
            event.score_key = score_key
            event.save()
            return CreateEvent(event)


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
#                  Main Mutation
#######################################################
class Mutation:
    # Create
    create_season = CreateSeason.Field()
    create_tournament = CreateTournament.Field()
    create_league = CreateLeague.Field()
    create_trainer = CreateTrainer.Field()
    create_event = CreateEvent.Field()

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
