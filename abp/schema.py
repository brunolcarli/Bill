import graphene


class Query(object):
    '''
        ABP Queries
    '''

    hello_bill = graphene.String()
    def resolve_hello_bill(self, info, **kwargs):
        return 'Hello buddy'
