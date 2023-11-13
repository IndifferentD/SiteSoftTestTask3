from database.handler import database_handler
from database.models import Hub, Article
import requests
from parser import HubPageParser
from logger import logger


def database_sync():
    logger.info("Syncing database tables")
    database_handler.connect()
    database_handler.create_tables([Hub, Article])

    hub_urls_to_parse = {
        'https://habr.com/ru/hubs/popular_science/articles/',
        'https://habr.com/ru/hubs/programming/articles/',
        'https://habr.com/ru/hubs/open_source/articles/',
        'https://habr.com/ru/hubs/maths/articles/'
    }
    hub_urls_to_parse_in_database = {hub.hub_url for hub in Hub.select()}
    for hub_url in hub_urls_to_parse:
        if hub_url not in hub_urls_to_parse_in_database:
            response = requests.get(hub_url)
            hub_page_parser = HubPageParser(response.text)
            hub_name = hub_page_parser.hub_title
            Hub.create(hub_name=hub_name, hub_url=hub_url)

    for hub_url in hub_urls_to_parse_in_database:
        if hub_url not in hub_urls_to_parse:
            Hub.delete().where(Hub.hub_url == hub_url).execute()

    database_handler.close()
    logger.info("Database tables successfully synced")
