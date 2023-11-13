from peewee import Model, CharField, DateTimeField,  AutoField,  TextField,  ForeignKeyField
from database.handler import database_handler


class BaseModel(Model):
    class Meta:
        database = database_handler


class Hub(BaseModel):
    id: int = AutoField(primary_key=True, null=False)
    hub_name: str = CharField(null=False)
    hub_url: str = CharField(null=False)

    class Meta:
        table_name = 'hubs'


class Article(BaseModel):
    id: int = AutoField(primary_key=True, null=False)
    hub_id: int = ForeignKeyField(Hub, on_delete='CASCADE')
    article_url: str = CharField(null=False)
    article_title: str = CharField(null=False)
    article_text: str = TextField(null=False)
    published_at = DateTimeField(null=False)
    author_username: str = CharField(null=False)
    author_url: str = CharField(null=False)

    @classmethod
    def is_in_database(cls, article_url):
        return cls.get_or_none(article_url == cls.article_url)

    class Meta:
        table_name = 'articles'
