"""
Models da aplicação civil-cultural.
Este módulo contém a definição das tabelas do banco de dados, gerenciadas
pelo ORM do django.

Os objetos definidos neste módulo representam o core do sistema, especificando
os elementos que o compõem e as relações que estes estabelecem entre si.
"""
from django.db import models
from django.contrib.auth import get_user_model


class Portal(models.Model):
    """
    Um portal é uma área do sistema que engloba a maior parte dos demais
    objetos. O portal conterá noticias, tópicos, regras próprias, assim como
    uma temática específica e membros participantes.
    """
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    founding_datetime = models.DateTimeField(
        auto_now_add=True
    )
    topics = models.ManyToManyField('civil_cultural.Topic')
    is_public = models.BooleanField(default=True)
    rules = models.ManyToManyField('civil_cultural.Rule')
    # TODO - add Chat
    users = models.ManyToManyField(get_user_model())
    tags = models.ManyToManyField('civil_cultural.Tag')
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='portal_owner'
    )


class Topic(models.Model):
    """
    Um tópico é uma especificação para um escopo de discussão dentro de um
    Portal. Os Portais poderão ter tópicos diversos para diferentes assuntos
    onde serão publicados artigos relacionados à temática definida pelo Tópico.
    """
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    description = models.TextField()
    scope = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    creation_datetime = models.DateTimeField(
        auto_now_add=True
    )
    articles = models.ManyToManyField('civil_cultural.Article')
    topic_portal = models.ForeignKey(
        'civil_cultural.Portal',
        on_delete=models.CASCADE,
    )
    # TODO - add Tag


class Article(models.Model):
    """
    Um artigo é uma publicação realizada por um perito ou especialista no
    assunto do Tópico. Os artigos são publicados em tópicos de acordo com a
    especificidade do assunto abordado.
    Um artigo pode conter perguntas realizadas por membros do Portal, que
    poderão ser respondidas e classificadas por votos.
    """
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    post_author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    article_authors = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )
    abstract = models.CharField(
        max_length=1500,
        unique=True
    )
    body = models.TextField(
        blank=False,
        null=False,
        unique=True
    )
    references = models.TextField()
    pro_votes = models.IntegerField(default=0)
    cons_votes = models.IntegerField(default=0)
    publication_date = models.DateField(
        auto_now_add=True
    )
    questions = models.ManyToManyField('civil_cultural.Question')
    tags = models.ManyToManyField('civil_cultural.Tag')
    reports = models.ManyToManyField('civil_cultural.Report')
    similar_suggestions = models.ManyToManyField(
        'civil_cultural.SimilarSuggestion'
    )
    published_topic= models.ForeignKey(
        'civil_cultural.Topic',
        on_delete=models.CASCADE
    )


class SimilarSuggestion(models.Model):
    """
    Uma sugestão similar é uma postagem em um tópico ou notíca agregando
    informação de outras materias que possuem similaridade com a postagem
    em questão.
    """
    class Meta:
        unique_together = ('link', 'post_key')

    post_author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    description = models.TextField()
    link = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )
    pro_votes = models.IntegerField(default=0)
    cons_votes = models.IntegerField(default=0)
    publish_datetime = models.DateTimeField(
        auto_now_add=True
    )
    post_key = models.CharField(max_length=50)


class Question(models.Model):
    """
    Uma questão (pergunta) é uma publicação em um artigo para resolução de
    dúvidas que o artigo possa ter levantado.
    """ 
    post_author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    pro_votes = models.IntegerField(default=0)
    cons_votes = models.IntegerField(default=0)
    publish_datetime = models.DateTimeField(
        auto_now_add=True
    )
    published_article = models.ForeignKey(
        'civil_cultural.Article',
        on_delete=models.CASCADE
    )
    # answers = models.ManyToManyField('civil_cultural.Answer')


class Report(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    description = models.TextField(
        blank=False,
        null=False
    )
    report_datetime = models.DateTimeField(
        auto_now_add=True
    )
    # TODO - add Problem
    # TODO - add ProblemType (maybe a choices)


class Rule(models.Model):
    """
    Uma regra é uma definição que estabelece no Portal uma delimitação
    que deve ser respeitada pelos membros participantes.
    """
    class Meta:
        unique_together = ('description', 'portal_reference')

    description = models.CharField(
        max_length=400,
        blank=False,
        null=False,
    )
    creation_date = models.DateField(
        auto_now_add=True
    )
    portal_reference = models.ForeignKey(
        Portal,
        on_delete=models.CASCADE
    )


class Tag(models.Model):
    """
    Uma tag é um marcador que classifica uma publicação de acordo com
    uma temática, é utilizada para filtrar elementos no sistema.
    """
    reference = models.CharField(
        max_length=80,
        blank=False,
        null=False,
        unique=True
    )


class News(models.Model):
    """
    Modelo de dados para publicação de uma notícia.
    """
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    pro_votes = models.IntegerField(default=0)
    cons_votes = models.IntegerField(default=0)
    publication_date = models.DateTimeField(auto_now_add=True)
    similar_suggestions = models.ManyToManyField(SimilarSuggestion)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
        )
    portal_reference = models.ForeignKey(Portal, on_delete=models.CASCADE)
    # TODO question


class Answer(models.Model):
    """
    Definição de uma resposta à uma questão que tenha sido publicada.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        null=True,
        blank=True    
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
    )
    pro_votes = models.IntegerField(default=0)
    cons_votes = models.IntegerField(default=0)
    publish_datetime = models.DateTimeField(
        auto_now_add=True
    )
