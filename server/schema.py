import graphene
import graphql_jwt

# import chatbot.schema as chatbot
import users.schema as users
import civil_cultural.schema as civil_cultural

queries = (
    graphene.ObjectType,
    # chatbot.Query,
    users.Query,
    civil_cultural.Query,
)

mutations = (
    graphene.ObjectType,
    # chatbot.Mutation,
    users.Mutation,
    civil_cultural.Mutation,
)

class Query(*queries):
    pass


class Mutation(*mutations):
    log_in = graphql_jwt.ObtainJSONWebToken.Field()
    validate_user_token = graphql_jwt.Verify.Field()
    refresh_user_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
