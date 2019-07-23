import graphene
import abp.schema as abp


queries = (
    graphene.ObjectType,
    abp.Query,
)

mutations = (
    graphene.ObjectType,
)

class Query(*queries):
    pass


# class Mutation(*mutations):
#     pass


schema = graphene.Schema(query=Query)
