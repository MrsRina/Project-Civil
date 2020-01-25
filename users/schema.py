"""
Schema contendo objetos de usuário para o sistema.
Neste módulo ficarão:
    - Objetos graphql;
    - Queries (consultas) relacionadas a usuários;
    - Mutations:
        + Para cadastro;
        + LogOut do sistema

By Beelzebruno <brunolcarli@gmail.com>
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from users.utils import is_adult, access_required
from black_list.models import TokenBlackList


class UserType(DjangoObjectType):
    """
    Modelo de usuário padrão do django
    """ 
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)


class UserConnection(graphene.relay.Connection):
    """Implementa o relay no objeto User."""
    class Meta:
        node = UserType


class Query(object):
    """
    Consultas GraphQL delimitando-se ao escopo
    de usuários.
    """
    users = graphene.relay.ConnectionField(UserConnection)

    @access_required
    def resolve_users(self, info, **kwargs):
        """
        Retorna uma lista de todos os usuários registrados no sistema.
        """
        return get_user_model().objects.all()


class CreateUser(graphene.relay.ClientIDMutation):
    """
    Cadastra um novo usuário no sistema.
    """
    user = graphene.Field(
        UserType,
        description='The response is a User Object.'
    )

    class Input:
        """inputs"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        birth_date = graphene.Date(requried=True)

    def mutate_and_get_payload(self, info, **_input):

        username = _input.get('username')
        password = _input.get('password')
        email = _input.get('email')
        birth_date = _input.get('birth_date')

        if not is_adult(birth_date):
            raise Exception('you need to be an adult to register!')

        try:
            user = get_user_model()(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
        except:
            raise Exception(
                'Username already registered. Please choose another username!'
            )
        return CreateUser(user=user)


class LogOut(graphene.relay.ClientIDMutation):
    """
    Desloga do sistema.
    """
    response = graphene.String()

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        meta_info = info.context.META
        user_token = meta_info.get('HTTP_AUTHORIZATION')

        revoke = TokenBlackList.objects.create(token=user_token)
        revoke.save()

        return LogOut("Bye Bye")


class Mutation(object):
    sign_up = CreateUser.Field()
    log_out = LogOut.Field()
