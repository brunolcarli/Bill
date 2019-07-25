import graphene
from abp.models import Season


class SeasonType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    description = graphene.String()

    # TODO add tournaments
    # TODO add league


class SeasonlConnection(graphene.relay.Connection):
    class Meta:
        node = SeasonType


class Query(object):
    '''
        ABP Queries
    '''
    node = graphene.relay.Node.Field()

    ###################################################
    #                       Seasons                   #
    ###################################################
    seasons = graphene.relay.ConnectionField(
        SeasonlConnection
    )
    def resolve_seasons(self, info, **kwargs):
        return Season.objects.all()
