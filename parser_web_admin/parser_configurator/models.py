from django.db import models


# Create your models here.
class Hub(models.Model):
    hub_name: str = models.CharField(null=False)
    hub_url: str = models.URLField(null=False)
    poll_interval: int = models.IntegerField(null=False, default=600)

    class Meta:
        # Specify the table name
        db_table = 'hubs'

    def __str__(self):
        return f'{self.id}: {self.hub_name}'


class Article(models.Model):
    hub_id: int = models.ForeignKey(Hub, on_delete=models.CASCADE, db_column='hub_id')
    article_url: str = models.URLField(null=False)
    article_title: str = models.CharField(null=False)
    article_text: str = models.TextField(null=False)
    published_at = models.DateTimeField(null=False)
    author_username: str = models.CharField(null=False)
    author_url: str = models.URLField(null=False)

    class Meta:
        # Specify the table name
        db_table = 'articles'

    def __str__(self):
        return f'{self.id}: {self.article_title}'
