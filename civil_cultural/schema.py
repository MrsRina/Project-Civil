"""
Schema da aplicação civil-cultural.
Este módulo contém:
    - Modelos de objetos graphql;
    - Queries (consultas);
    - Mutations:
        + Creates;
        + Updates;
        + Deletes;

By: BeelzeBruno <brunolcarli@gmail.com>
"""
import graphene
from graphql_relay import from_global_id

from users.schema import UserType, UserConnection
from civil_cultural.models import (Portal, Topic, Article, Question, Tag, Rule,
                                    SimilarSuggestion, News, Answer)

from users.utils import access_required



##########################################################################
# GraphQl Objects
##########################################################################
class PortalType(graphene.ObjectType):
    """
    Defines a GraphQl Portal object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    founding_datetime = graphene.DateTime()
    topics = graphene.ConnectionField('civil_cultural.schema.TopicConnection')
    news = graphene.ConnectionField('civil_cultural.schema.NewsConnection')
    rules = graphene.ConnectionField('civil_cultural.schema.RuleConnection')
    members = graphene.ConnectionField(UserConnection)
    is_public = graphene.Boolean()
    # TODO - add Chat
    # TODO - add Tags
    owner = graphene.Field(UserType)

    def resolve_topics(self, info, **kwargs):
        return self.topic_set.all()

    def resolve_rules(self, info, **kwargs):
        return self.rule_set.all()

    def resolve_news(self, info, **kwargs):
        return self.news_set.all()

    def resolve_members(self, info, **kwargs):
        return self.users.all()


class PortalConnection(graphene.relay.Connection):
    class Meta:
        node = PortalType


class TopicType(graphene.ObjectType):
    """
    Defines a GraphQl Topic object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    description = graphene.String()
    scope = graphene.String()
    creation_datetime = graphene.DateTime()
    portal = graphene.Field(
        PortalType
    )
    # TODO - add Tags
    articles = graphene.List(
        'civil_cultural.schema.ArticleType'
    )

    def resolve_portal(self, info, **kwargs):
        return self.topic_portal

    def resolve_articles(self, info, **kwargs):
        return self.article_set.all()


class TopicConnection(graphene.relay.Connection):
    class Meta:
        node = TopicType


class ArticleType(graphene.ObjectType):
    """
    Defines an Article GraphQl object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    title = graphene.String()
    publication_date = graphene.DateTime()
    post_author = graphene.Field(
        UserType,
        description='User that published the article.'
    )
    article_authors = graphene.List(
        graphene.String
    )
    abstract = graphene.String()
    body = graphene.String()
    pro_votes = graphene.Int()
    cons_votes = graphene.Int()
    references = graphene.String()
    questions = graphene.ConnectionField(
        'civil_cultural.schema.QuestionConnection'
    )
    # TODO add tags
    # TODO reports
    similar_suggestions = graphene.ConnectionField(
        'civil_cultural.schema.SimilarSuggestionConnection'
    )

    def resolve_article_authors(self, info, **kwargs):
        return [author for author in self.article_authors.split(';')]

    def resolve_questions(self, info, **kwargs):
        return self.question_set.all()

    def resolve_similar_suggestions(self, info, **kwargs):
        return self.similar_suggestions.all()


class ArticleConnection(graphene.relay.Connection):
    class Meta:
        node = ArticleType


class QuestionType(graphene.ObjectType):
    """
    Defines an Question GraphQl object.
    A question is related to a specific Article
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    post_author = graphene.Field(
        UserType,
        description='User that published the question.'
    )
    text = graphene.String()
    pro_votes = graphene.Int()
    cons_votes = graphene.Int()
    publish_datetime = graphene.DateTime()
    article = graphene.Field('civil_cultural.schema.ArticleType')
    answers = graphene.relay.ConnectionField(
        'civil_cultural.schema.AnswerConnection'
    )

    def resolve_article(self, info, **kwargs):
        return self.published_article

    def resolve_answers(self, info, **kwargs):
        return self.answer_set.all()


class QuestionConnection(graphene.relay.Connection):
    class Meta:
        node = QuestionType


class TagType(graphene.ObjectType):
    """
    Defines an Tag GraphQl object.
    A tag is related to a specific subject matter.
    Can be used to filter and group objects.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    reference = graphene.String()


class TagConnection(graphene.relay.Connection):
    class Meta:
        node = TagType


class RuleType(graphene.ObjectType):
    """
    Defines an Rule GraphQl object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    description = graphene.String()
    creation_date = graphene.Date()
    portal = graphene.Field(PortalType)

    def resolve_portal(self, info, **kwargs):
        return self.portal_reference


class RuleConnection(graphene.relay.Connection):
    class Meta:
        node = RuleType


class NewsType(graphene.ObjectType):
    """
    Representação de uma Noticia
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    # atributos
    title = graphene.String(
        description='News title.'
    )
    body = graphene.String(
        description='News main content.'
    )
    pro_votes = graphene.Int(
        description='Positive votes this news has received.'
    )
    cons_votes = graphene.Int(
        description='Negative otes this news has received.'
    )
    publication_date = graphene.DateTime(
        description='Publish datetime.'
    )
    author = graphene.Field(
        UserType,
        description='News author.'
    )
    portal = graphene.Field(
        PortalType
    )
    similar_suggestions = graphene.ConnectionField(
        'civil_cultural.schema.SimilarSuggestionConnection'
    )
    # TODO question

    def resolve_portal(self, info, **Kwargs):
        return self.portal_reference

    def resolve_similar_suggestions(self, info, **kwargs):
        return self.similar_suggestions.all()

    # @classmethod
    # def get_node(cls, info, id):
    #     return get_news(id=id)


class NewsConnection(graphene.relay.Connection):
    class Meta:
        node = NewsType


class SimilarSuggestionType(graphene.ObjectType):
    """
    Defines an Similar Suggestion GraphQl object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    post_author = graphene.Field(
        UserType
    )
    description = graphene.String()
    link = graphene.String()
    pro_votes = graphene.Int()
    cons_votes = graphene.Int()
    publish_datetime = graphene.DateTime()


class SimilarSuggestionConnection(graphene.relay.Connection):
    class Meta:
        node = SimilarSuggestionType


class AnswerType(graphene.ObjectType):
    """
    Defines an Answer post GraphQl object.
    """
    class Meta:
        interfaces = (graphene.relay.Node,)

    post_author = graphene.Field(
        UserType
    )
    text = graphene.String()
    pro_votes = graphene.Int()
    cons_votes = graphene.Int()
    publish_datetime = graphene.DateTime()
    question = graphene.Field(
        QuestionType
    )

    def resolve_question(self, info, **kwargs):
        return self.question

    def resolve_post_author(self, info, **kwargs):
        return self.author


class AnswerConnection(graphene.relay.Connection):
    class Meta:
        node = AnswerType


##########################################################################
# Schema QUERY
##########################################################################
class Query(object):
    """
    Queries for civil_cultural.
    """
    node = graphene.relay.Node.Field()

    portals = graphene.relay.ConnectionField(
        PortalConnection
    )

    @access_required
    def resolve_portals(self, info, **kwargs):
        """
        Returns all portals from civil cultural.
        """
        return Portal.objects.all()

    topics = graphene.relay.ConnectionField(
        TopicConnection
    )

    @access_required
    def resolve_topics(self, info, **kwargs):
        """
        Returns all topics from civil cultural.
        """
        return Topic.objects.all()

    articles = graphene.relay.ConnectionField(
        ArticleConnection
    )

    @access_required
    def resolve_articles(self, info, **kwargs):
        return Article.objects.all()

    questions = graphene.relay.ConnectionField(
        QuestionConnection
    )

    @access_required
    def resolve_questions(self, info, **kwargs):
        return Question.objects.all()

    tags = graphene.relay.ConnectionField(TagConnection) 

    @access_required
    def resolve_tags(self, info, **kwargs):
        return Tag.objects.all()

    rules = graphene.relay.ConnectionField(RuleConnection)

    @access_required
    def resolve_rules(self, info, **kwargs):
        return Rule.objects.all()

    similar_suggestions = graphene.relay.ConnectionField(
        SimilarSuggestionConnection
    )

    @access_required
    def resolve_similar_suggestions(self, info, **kwargs):
        return SimilarSuggestion.objects.all()

    news = graphene.relay.ConnectionField(
        NewsConnection,
        author=graphene.Int(
            description="Author's integer ID."
        ),
        title_contains=graphene.String(
            description='The title must contain...'
        ),
        body_contains=graphene.String(
            description='Body text must contain...'
        )
    )

    @access_required
    def resolve_news(self, info, **kwargs):
        """
        Retorna uma lista de noticias registradas
        no sistema.
        """
        # filtros
        author = kwargs.get('author')
        title_contains = kwargs.get('title_contains')
        body_contains = kwargs.get('body_contains')

        # se fornecer filtro por autor, traz somente as noticias do autor
        if author:
            news = News.objects.filter(author=author)

        else:
            news = News.objects.all()

            if title_contains and body_contains:
                filtered_news = [
                    n for n in news if title_contains.lower() in n.title.lower()
                ]
                filtered_news += [
                    n for n in news if body_contains.lower() in n.body.lower()
                ]
                return filtered_news

            else:
                if title_contains and not body_contains:
                    news = [
                        n for n in news if title_contains.lower() in n.title.lower()
                    ]

                if body_contains and not title_contains:
                    news = [
                        n for n in news if body_contains.lower() in n.body.lower()
                    ]
        return news

    answers = graphene.relay.ConnectionField(
        AnswerConnection
    )

    @access_required
    def resolve_answers(self, info, **kwargs):
        return Answer.objects.all()


##########################################################################
# MUTATION - Create
##########################################################################
class CreatePortal(graphene.relay.ClientIDMutation):
    """
    Creates a portal
    """
    portal = graphene.Field(
        PortalType,
        description='Created portal data response.'
    )

    class Input:
        name = graphene.String(
            description='Portal title.',
            required=True
        )
        is_public = graphene.Boolean()

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura dos inputs
        name = _input.get('name')
        is_public = _input.get('is_public', True)
        # identifica o usuario
        user = info.context.user

        try:
            portal = Portal.objects.create(
                name=name,
                owner=user,
                is_public=is_public
            )
            portal.users.add(user)
            portal.save()

            return CreatePortal(portal)

        except Exception as exception:
            raise(exception)


class CreateTopic(graphene.relay.ClientIDMutation):
    """
    Craates a topic
    """
    topic = graphene.Field(
        TopicType,
        description='Created topic data response.'
    )

    class Input:
        name = graphene.String(
            required=True,
            description='Topic title.'
        )
        description = graphene.String(
            description='Topic description.'
        )
        scope = graphene.String(
            description='Topic focus and scope.'
        )
        portal = graphene.ID(
            required=True,
            description='Topic portal ID.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura dos inputs
        name = _input.get('name')
        description = _input.get('description', '')
        scope = _input.get('scope', '')
        portal_id = _input.get('portal')

        _, portal_id = from_global_id(portal_id)

        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception(
                'Given portal does not exist!'
            )

        try:
            topic = Topic.objects.create(
                name=name,
                description=description,
                scope=scope,
                topic_portal=portal
            )
            topic.save()
            return CreateTopic(topic)

        except Exception as exception:
            raise(exception)


class CreateArticle(graphene.relay.ClientIDMutation):
    """
    Creates an Article
    """
    article = graphene.Field(
        ArticleType,
        description='Created article data response.'
    )

    class Input:
        title = graphene.String(
            requried=True,
            description='Article title.'
        )
        article_authors = graphene.List(
            graphene.String,
            required=True
        )
        abstract = graphene.String()
        body = graphene.String(
            requried=True
        )
        references = graphene.String(
            required=True
        )
        topic = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura dos inputs
        title = _input.get('title')
        article_authors = _input.get('article_authors', '')
        abstract = _input.get('abstract')
        body = _input.get('body')
        references = _input.get('references')
        topic = _input.get('topic')
        _, topic_id = from_global_id(topic)

        authors = ';'.join(author for author in article_authors)

        # identifica o usuario
        user = info.context.user

        try:
            topic = Topic.objects.get(
                id=topic_id
            )
        except Topic.DoesNotExist:
            raise Exception('Given topic does not exists.')

        try:
            article = Article.objects.create(
                title=title,
                abstract=abstract,
                body=body,
                references=references,
                post_author=user,
                article_authors=authors,
                published_topic=topic
            )
            article.save()

            return CreateArticle(article)

        except Exception as exception:
            raise(exception)


class CreateQuestion(graphene.relay.ClientIDMutation):
    """
    Creates an Question on an Article
    """
    question = graphene.Field(
        QuestionType,
        description='Created article data response.'
    )

    class Input:
        text = graphene.String(
            requried=True,
            description='Question text.'
        )
        article = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura dos inputs
        text = _input.get('text')
        article = _input.get('article')
        _, article_id = from_global_id(article)

        # identifica o usuario
        user = info.context.user

        try:
            article = Article.objects.get(
                id=article_id
            )
        except Article.DoesNotExist:
            raise Exception('Given article does not exists.')

        try:
            question = Question.objects.create(
                text=text,
                post_author=user,
                published_article=article
            )
            question.save()

            return CreateQuestion(question)

        except Exception as exception:
            raise(exception)


class CreateTag(graphene.relay.ClientIDMutation):
    """
    Creates a Tag
    """
    tag = graphene.Field(
        TagType,
        description='Created Tag data.'
    )

    class Input:
        reference = graphene.String(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')

        try:
            tag = Tag.objects.create(
                reference=reference
            )
            tag.save()
            return CreateTag(tag)

        # TODO - handle the right exception when the time comes
        except Exception:    
            raise Exception(
                "Impossible to create this tag. \
                Maybe this reference already exists."
            )


class CreateRule(graphene.relay.ClientIDMutation):
    """
    Creates a Rule
    """
    rule = graphene.Field(RuleType)

    class Input:
        description = graphene.Field(
            graphene.String,
            required=True
        )
        portal = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        description = _input.get('description')
        portal_id = _input.get('portal')
        _, portal_id = from_global_id(portal_id)

        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception('The given Portal does not exist.')

        try:
            rule = Rule.objects.create(
                description=description,
                portal_reference=portal
            )
            rule.save()
            return CreateRule(rule)
        except Exception:    
            raise Exception(
                "Impossible to create this rule. \
                Maybe it already exists."
            )


class CreateNews(graphene.relay.ClientIDMutation):
    """
    Cria uma Noticia
    """
    news = graphene.Field(
        NewsType,
        description='Created news data response.'
    )

    class Input:
        title = graphene.String(description='News title.')
        body = graphene.String(description='News main content.')
        portal = graphene.ID(
            required=True,
            description='Topic portal ID.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura dos inputs
        title = _input.get('title')
        body = _input.get('body')
        portal_id = _input.get('portal')
        _, portal_id = from_global_id(portal_id)

        try:
            portal = Portal.objects.get(id=portal_id)

        except Portal.DoesNotExist:
            raise Exception('The given portal does not exist.')

        try:
            news = News.objects.create(
                title=title,
                body=body,
                author=info.context.user,
                portal_reference=portal
            )
            news.save()

            return CreateNews(news)

        except Exception as exception:
            raise(exception)


class CreateSimilarSuggestion(graphene.relay.ClientIDMutation):
    """
    Creates a similar suggestion post.
    """
    similar_suggestion = graphene.Field(
        SimilarSuggestionType
    )

    class Input:
        description = graphene.String()
        link = graphene.String(required=True)
        post_id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        description = _input.get('description')
        link = _input.get('link')
        post_key = _input.get('post_id')

        # identifica o usuario
        user = info.context.user

        # Manobra arriscada // risky trick // @mcgyver
        post_type, post_id = from_global_id(post_key)
        if post_type == 'NewsType':

            try:
                post = News.objects.get(id=post_id)
            except News.DoesNotExist:
                raise Exception('Given post does not exist.')

        elif post_type == 'ArticleType':
            try:
                post = Article.objects.get(id=post_id)
            except Article.DoesNotExist:
                raise Exception('Given post does not exist.')

        else:
            raise Exception('Ivalid Post ID!')

        try:
            similar_suggestion = SimilarSuggestion.objects.create(
                post_author=user,
                description=description,
                link=link,
                post_key=post_key
            )
        except Exception as ex:
            raise ex

        try:
            similar_suggestion.save()
            post.similar_suggestions.add(similar_suggestion)
            post.save()
            return CreateSimilarSuggestion(similar_suggestion)
        except Exception as ex:
            raise ex


class CreateAnswer(graphene.relay.ClientIDMutation):
    """
    Creates a answer.
    """
    answer = graphene.Field(
        AnswerType
    )

    class Input:
        text = graphene.String(requried=True)
        question = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        text = _input.get('text')
        _id = _input.get('question')
        _, question_id = from_global_id(_id)

        # identifica o usuario
        user = info.context.user

        try:
            question = Question.objects.get(
                id=question_id
            )
        except Question.DoesNotExist:
            raise Exception('Given question does not exists.')

        try:
            answer = Answer.objects.create(
                text=text,
                author=user,
                question=question
            )
            answer.save()

            return CreateAnswer(answer)

        except Exception as exception:
            raise(exception)


##########################################################################
# MUTATION - Update
##########################################################################
class UpdateNews(graphene.relay.ClientIDMutation):
    """
    Updates a published News.
    """
    news = graphene.Field(
        NewsType,
        description='Updated news data response.'
    )

    class Input:
        title = graphene.String(description='News title.', required=False)
        body = graphene.String(description='News main content.', requried=False)
        id = graphene.ID(description='News ID.', required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        # captura os inputs
        title = _input.get('title')
        body = _input.get('body')
        _, id = from_global_id(_input.get('id'))

        # identifica o usuario
        user = info.context.user

        # recupera o objeto do banco de dados
        try:
            news = News.objects.get(id=id)
        except Exception as exception:
            raise(exception)

        # somente poderá modificar o objeto se for o autor do mesmo
        if not news.author.id == user.id:
            raise Exception("You don't have permission to do this.")

        # atualiza o objeto
        if title:
            news.title = title
        if body:
            news.body = body
        news.save()

        return UpdateNews(news)


class UpdatePortal(graphene.relay.ClientIDMutation):
    """
    Updates a Portal.
    """
    portal = graphene.Field(
        PortalType,
        description='Updated Portal data response.'
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Portal ID.'
        )
        name = graphene.String(
            requried=True
        )
        # TODO add is_public

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        portal_id = _input.get('id')
        name = _input.get('name')

        _, portal_id = from_global_id(portal_id)
        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception('Given Portal ID does not exist!')
        else:
            portal.name = name
            portal.save()
        return UpdatePortal(portal)


class UpdateTopic(graphene.ClientIDMutation):
    """
    Updates a Topic.
    """
    topic = graphene.Field(
        TopicType,
        description='Updated Topic data response.'
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Topic ID.'
        )
        name = graphene.String(
            description='Changes the Topic name.'
        )
        description = graphene.String(
            description='Changes the Topic description.'
        )
        scope = graphene.String(
            description='Changes the Topic scope.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        name = _input.get('name')
        description = _input.get('description')
        scope = _input.get('scope')
        _id = _input.get('id')
        _, topic_id = from_global_id(_id)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise Exception('Given Topic does not exist.')

        else:
            if name:
                topic.name = name
            if description:
                topic.description = description
            if scope:
                topic.scope = scope
            topic.save()
            return UpdateTopic(topic)


class UpdateRule(graphene.ClientIDMutation):
    """
    Updates a portal Rule.
    """
    rule = graphene.Field(
        RuleType,
        description='Updated rule.'
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        description = graphene.String(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        description = _input.get('description')
        _id = _input.get('id')
        _, rule_id = from_global_id(_id)

        try:
            rule = Rule.objects.get(id=rule_id)
        except Rule.DoesNotExist:
            raise Exception('Given Rule does not exist.')
        else:
            rule.description = description
            rule.save()
            return UpdateRule(rule)


class UpdateArticle(graphene.ClientIDMutation):
    """
    Updates a published article.
    """
    article = graphene.Field(
        ArticleType,
        description='Updated article data.'
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        title = graphene.String()
        article_authors = graphene.List(
            graphene.String
        )
        abstract = graphene.String()
        body = graphene.String()
        references = graphene.String()

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        title = _input.get('title')
        abstract = _input.get('abstract')
        body = _input.get('body')
        references = _input.get('references')
        article_authors = _input.get('article_authors')
        _id = _input.get('id')
        _, article_id = from_global_id(_id)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise Exception('Given article does not exist.')
        else:

            if title:
                article.title = title
            if abstract:
                article.abstract = abstract
            if body:
                article.body = body
            if references:
                article.refereces = references
            if article_authors:
                authors = ';'.join(author for author in article_authors)
                article.article_authors = authors
            article.save()
            return UpdateArticle(article)


class UpdateQuestion(graphene.ClientIDMutation):
    """
    Updates a question.
    """
    question = graphene.Field(
        QuestionType
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Question ID.'
        )
        text = graphene.String(
            required=True,
            description='Text to update'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        text = _input.get('text')
        _id = _input.get('id')
        _, question_id = from_global_id(_id)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Exception('Sorry, the given question does not exist!')

        else:
            question.text = text
            question.save()
            return UpdateQuestion(question)


class UpdateTag(graphene.ClientIDMutation):
    """
    Updates a Tag.
    """
    tag = graphene.Field(
        TagType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        reference = graphene.String(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        reference = _input.get('reference')
        _id = _input.get('id')
        _, tag_id = from_global_id(_id)

        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise Exception('Sorry, the given tag does not exist.')
        else:
            tag.reference = reference
            tag.save()
            return UpdateTag(tag)


class UpdateSuggestion(graphene.ClientIDMutation):
    """
    Updates a Similar Suggestion
    """
    similar_suggestion = graphene.Field(
        SimilarSuggestionType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        description = graphene.String()
        link = graphene.String()

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        description = _input.get('description')
        link = _input.get('link')
        _id = _input.get('id')
        _, suggestion_id = from_global_id(_id)

        try:
            suggestion = SimilarSuggestion.objects.get(id=suggestion_id)
        except SimilarSuggestion.DoesNotExist:
            raise Exception('Given Suggestion does not exist.')

        else:
            if description:
                suggestion.description = description
            if link:
                suggestion.link = link
            suggestion.save()
            return UpdateSuggestion(suggestion)


class UpdateAnswer(graphene.relay.ClientIDMutation):
    """
    Updates a created answer.
    """
    answer = graphene.Field(
        AnswerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )
        text = graphene.String(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        text = _input.get('text')
        _id = _input.get('id')
        object_type, answer_id = from_global_id(_id)

        if not object_type == 'AnswerType':
            raise Exception('Invalid ID: The given ID is not a Answer ID!')

        if not text:
            raise Exception('The text must not be blank! Write something.')

        # Tenta recuperar o objeto do banco de dados
        try:
            answer = Answer.objects.get(
                id=answer_id
            )
        except Answer.DoesNotExist:
            raise Exception('Given answer does not exists.')

        # identifica o usuario
        user = info.context.user

        # somente poderá modificar o objeto se for o autor do mesmo
        if not answer.author.id == user.id:
            raise Exception("You don't have permission to do this.")

        try:
            answer.text = text
            answer.save()

        except Exception as exception:
            raise(exception)

        return UpdateAnswer(answer)


##########################################################################
# MUTATION - Delete
##########################################################################
class DeleteNews(graphene.relay.ClientIDMutation):
    """
    Remove uma Notícia.
    """
    news = graphene.Field(
        NewsType,
        description='Deleted News.'
    )

    class Input:
        id = graphene.ID(description='ID da notícia', required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _, id = from_global_id(_input.get('id'))
        # identifica o usuario
        user = info.context.user

        # recupera o objeto do banco de dados
        try:
            news = News.objects.get(id=id)
        except Exception as exception:
            raise(exception)

        # somente poderá modificar o objeto se for o autor do mesmo
        if not news.author.id == user.id:
            raise Exception("You don't have permission to do this.")

        deleted_data = news
        news.delete()
        return DeleteNews(deleted_data)


class DeletePortal(graphene.relay.ClientIDMutation):
    """
    Deletes a Portal.
    """
    portal = graphene.Field(
        PortalType,
        description='Deleted Portal data response.'
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Portal ID.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        portal_id = _input.get('id')
        _, portal_id = from_global_id(portal_id)

        # TODO verificar se o user é dono do portal

        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception('Given Portal ID does not exist!')
        else:
            portal.delete()

        return DeletePortal(portal)


class DeleteTopic(graphene.ClientIDMutation):
    """
    Deletes a Topic.
    """
    topic = graphene.Field(
        TopicType,
        description='Deleted Topic data response.'
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Topic ID.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, topic_id = from_global_id(_id)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise Exception('Given Topic does not exist.')

        else:
            topic.delete()
            return DeleteTopic(topic)


class DeleteRule(graphene.ClientIDMutation):
    """
    Deletes a portal Rule.
    """
    rule = graphene.Field(
        RuleType,
        description='Deleted rule.'
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, rule_id = from_global_id(_id)

        try:
            rule = Rule.objects.get(id=rule_id)
        except Rule.DoesNotExist:
            raise Exception('Given Rule does not exist.')
        else:
            rule.delete()
            return DeleteRule(rule)


class DeleteArticle(graphene.ClientIDMutation):
    """
    Deletes a published article.
    """
    article = graphene.Field(
        ArticleType,
        description='Deleted article data.'
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, article_id = from_global_id(_id)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise Exception('Given article does not exist.')
        else:
            article.delete()
            return DeleteArticle(article)


class DeleteQuestion(graphene.ClientIDMutation):
    """
    Deletes a question.
    """
    question = graphene.Field(
        QuestionType
    )

    class Input:
        id = graphene.ID(
            required=True,
            description='Question ID.'
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, question_id = from_global_id(_id)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Exception('Sorry, the given question does not exist!')

        else:
            question.delete()
            return DeleteQuestion(question)


class DeleteTag(graphene.ClientIDMutation):
    """
    Deletes a Tag.
    """
    tag = graphene.Field(
        TagType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, tag_id = from_global_id(_id)

        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise Exception('Sorry, the given tag does not exist.')
        else:
            tag.delete()
            return DeleteTag(tag)


class DeleteSuggestion(graphene.ClientIDMutation):
    """
    Deletes a Similar Suggestion
    """
    similar_suggestion = graphene.Field(
        SimilarSuggestionType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        _, suggestion_id = from_global_id(_id)

        try:
            suggestion = SimilarSuggestion.objects.get(id=suggestion_id)
        except SimilarSuggestion.DoesNotExist:
            raise Exception('Given Suggestion does not exist.')

        else:
            suggestion.delete()
            return DeleteSuggestion(suggestion)


class DeleteAnswer(graphene.relay.ClientIDMutation):
    """
    Deletes a created answer.
    """
    answer = graphene.Field(
        AnswerType
    )

    class Input:
        id = graphene.ID(
            required=True
        )

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('id')
        object_type, answer_id = from_global_id(_id)

        if not object_type == 'AnswerType':
            raise Exception('Invalid ID: The given ID is not a Answer ID!')

        # Tenta recuperar o objeto do banco de dados
        try:
            answer = Answer.objects.get(
                id=answer_id
            )
        except Answer.DoesNotExist:
            raise Exception('Given answer does not exists.')

        # identifica o usuario
        user = info.context.user

        # somente poderá modificar o objeto se for o autor do mesmo
        if not answer.author.id == user.id:
            raise Exception("You don't have permission to do this.")

        answer.delete()

        return DeleteAnswer(answer)


##########################################################################
# Other Stuff
##########################################################################
class JoinPortal(graphene.relay.ClientIDMutation):
    """
    Join a Portal as member.
    """
    portal = graphene.Field(PortalType)

    class Input:
        portal_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('portal_id')
        object_type, portal_id = from_global_id(_id)

        if not object_type == 'PortalType':
            raise Exception('Invalid ID: The given ID is not a Portal ID!')

        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception('Given Portal ID does not exist!')

        # identifica o usuario
        user = info.context.user
        if user in portal.users.all():
            raise Exception('This user is already a member of this portal!')
        else:
            portal.users.add(user)
            portal.save()

        return JoinPortal(portal)


class LeavePortal(graphene.relay.ClientIDMutation):
    """
    Leaves a Portal membership.
    """
    portal = graphene.Field(PortalType)

    class Input:
        portal_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        _id = _input.get('portal_id')
        object_type, portal_id = from_global_id(_id)

        if not object_type == 'PortalType':
            raise Exception('Invalid ID: The given ID is not a Portal ID!')

        try:
            portal = Portal.objects.get(id=portal_id)
        except Portal.DoesNotExist:
            raise Exception('Given Portal ID does not exist!')

        # identifica o usuario
        user = info.context.user
        if user in portal.users.all():
            portal.users.remove(user)
        else:
            raise Exception('Your not a member of this Portal!')

        return LeavePortal(portal)


##########################################################################
# Schema Mutation
##########################################################################
class Mutation:
    # Create
    create_portal = CreatePortal.Field()
    create_topic = CreateTopic.Field()
    create_article = CreateArticle.Field()
    create_question = CreateQuestion.Field()
    create_tag = CreateTag.Field()
    create_rule = CreateRule.Field()
    create_news = CreateNews.Field()
    create_similar_suggestion = CreateSimilarSuggestion.Field()
    create_answer = CreateAnswer.Field()

    # Update
    update_news = UpdateNews.Field()
    update_portal = UpdatePortal.Field()
    update_topic = UpdateTopic.Field()
    update_rule = UpdateRule.Field()
    update_article = UpdateArticle.Field()
    update_question = UpdateQuestion.Field()
    update_tag = UpdateTag.Field()
    update_similar_suggestion = UpdateSuggestion.Field()
    update_answer = UpdateAnswer.Field()

    # Delete
    delete_news = DeleteNews.Field()
    delete_portal = DeletePortal.Field()
    delete_topic = DeleteTopic.Field()
    delete_rule = DeleteRule.Field()
    delete_article = DeleteArticle.Field()
    delete_question = DeleteQuestion.Field()
    delete_tag = DeleteTag.Field()
    delete_similar_suggestion = DeleteSuggestion.Field()
    delete_answer = DeleteAnswer.Field()

    # Other stuff
    join_portal = JoinPortal.Field()
    leave_portal = LeavePortal.Field()
