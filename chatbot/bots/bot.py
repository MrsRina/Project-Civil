# -*- coding: utf-8 -*-
'''
Chatbot simples que aprende de uma lista.
'''

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

cid = ChatBot('Cid')

trainer = ListTrainer(cid)
trainer.train([
    "Hello",
    "Oh hello there.",
    "Who are you?",
    "I am Cid, a Chatbot built for helping human interaction."
])
