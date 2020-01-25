import graphene
from chatbot.bots.bot import cid
from chatbot.bots.nlp_bot import response, greeting, sent_tokens
from users.utils import access_required

class Query(object):
    
    show_me_the_sight_beyond_sight = graphene.List(
        graphene.String,
        description='This is an easter egg.'
    )

    def resolve_show_me_the_sight_beyond_sight(self, info, **kwargs):
        '''
        Resolve o easter egg e devolve o olho de thundera.
        '''
        the_eye_of_thundera = [
        '░░░░░░░▄▄▀▀▀▀▀▀▀▀▀▀▀▀▄▄░░░░░░░',
        '░░░░░▄▀░░░░░░░░░░░▄▄▄░░▀▄░░░░░',
        '░░░▄▀░░░░░░░░░▄▄███▀▄██▄░▀▄░░░',
        '░░█░░░░░░░░▄█████▄▄█████▄░░█▄░',
        '░█░░░░░░░▄█▀▄████████████▄░░█░',
        '░█░░░░▄█████████████▄▀████░░█░',
        '░█░░▄█████████████████░███░░█░',
        '░█░░█████▀░░░░░███████▀███░░█░',
        '░▀▄░▀███░░░░░░░██████▀░░▀▀░░█░',
        '░░▀▄░░▀█▄░░░░░▄██▀▀░░░░░░░░░█░',
        '░░░▀▄░░░░░▄▄▄████▄▄░░░░░░░▄▀░░',
        '░░░░░▀▄▄░░░▀▀▀▀▀▀▀░░░░░░▄▀░░░░',
        '░░░░░░░░▀▀▄▄▄▄▄▄▄▄▄▄▀▀▀░░░░░░░'
    ]
        return the_eye_of_thundera


class AskListBot(graphene.relay.ClientIDMutation):
    '''
    Realiza uma requisição ao bot que aprende de listas.
    '''

    response = graphene.String(description='List Bot response.')

    class Input:
        question = graphene.String(description='Input question.')

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        '''
        Algoritmo para resolução de uma pergunta ao bot simples
        que aprende de uma lista.
        '''

        question = _input.get('question')
        if question:
            return AskListBot(cid.get_response(question))

        return AskListBot("Sorry, i don't understand your question")


class AskNlpBot(graphene.relay.ClientIDMutation):
    '''
    Requisição ao bot que aprende por processamento
    de linguagem natural.
    '''
    response = graphene.String(description='Bot response.')

    class Input:
        question = graphene.String(description='Input question')

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        '''
        Algoritmo de resolução para requisições ao bot
        de processamento de linguagem natural.
        '''

        question = _input.get('question')

        # se o input for uma despedida
        if(question == 'Bye'):
            bot_response = 'BYE...TAKE CARE......'

        else:
            # se o input for um cumprimento
            if(greeting(question)):
                bot_response = greeting(question)

            else:
                bot_response = response(question)
                sent_tokens.remove(question)

        return AskNlpBot(bot_response)


class Mutation(object):
    ask_list_bot = AskListBot.Field()
    ask_nlp_bot = AskNlpBot.Field()
