# -*- coding: utf-8 -*-
import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# debug TODO remove this later
print("*"*100,os.getcwd(),"*"*100,)

def lem_tokens(tokens):
    '''
    Lematiza uma string de tokens recebidos.
    :param tokens: <str>
    rtype: <list>
    '''
    return [lemmer.lemmatize(token) for token in tokens]

def lem_normalize(text):
    '''
    Normaliza uma cadeia de caracteres.
    param text: <str>
    rtype: <list>
    '''
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    '''
    Retorna um cumprimento aleatório.

    param sentence: <str>
    rtype: <str>
    '''

    GREETINGS_INPUTS = (
        "hello", "hi", "grettings", "sup", "what's up", "hey",
    )
    GREETINGS_RESPONSES =[
        "hi", "hey", "*nods*", "hi there","hello", "i'm so glad"
    ]

    for word in sentence.split():
        if word.lower() in GREETINGS_INPUTS:
            return random.choice(GREETINGS_RESPONSES)

def response(user_input):
    '''
    Retorna uma resposta com base no conteúdo aprendido pelo bot.
    param user_input: <str>
    rtype: <str>
    '''
    bot_response = ''
    sent_tokens.append(user_input)

    # TODO melhorar o nome destas variáveis

    # Converte uma coleção de textos brutos para uma matriz de atributos TF-IDF.
    tf_id_matrix = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')

    # Aprende o vocabulário
    learned_set = tf_id_matrix.fit_transform(sent_tokens)

    # computa a semelhança do cosseno
    values_array = cosine_similarity(learned_set[-1], learned_set)

    idx = values_array.argsort()[0][-2]
    flat = values_array.flatten()
    flat.sort()
    threshold = flat[-2]

    if(threshold == 0):
        bot_response += "I can't undesteand you"
    else:
        bot_response += sent_tokens[idx]

    return bot_response

# Não sei se é uma boa idéia deixar esses downloads aqui :thinking:
nltk.download('punkt')
nltk.download('wordnet')

# TODO import this variable from a config file
files_to_read = ('server/chatbot/bots/copus.txt',)

# TODO Fazer com que esse bot leia de um diretorio de arquivos,
# ou uma lista de arquivos carregada por uma função, ou ainda
# ler diretamente do banco de dados
raw = ''
for path in files_to_read:
    with open(path, 'r', errors='ignore') as f:
        raw += f.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)