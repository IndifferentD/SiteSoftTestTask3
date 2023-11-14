import asyncio
import datetime
from collections import defaultdict

import aiohttp
import requests
from time import sleep
from database.init import database_sync
from database.models import Hub, Article
from http_client import fetch_html
from parser import HubPageParser, ArticlePageParser
from logger import logger

HABR_URL = 'https://habr.com'
PARALLEL_REQUESTS = 5

# словарь меток последнего парсинга хабов
last_parse_date = defaultdict(datetime.datetime)



async def parse_hub(hub: Hub):
    logger.info(f'Hub {hub.id}: {hub.hub_name} | checking for new articles ')
    hub_page_response = requests.get(hub.hub_url)
    hub_page_source = hub_page_response.text
    hub_page_parser = HubPageParser(hub_page_source)
    article_urls_to_parse = []
    for article_path in hub_page_parser.article_paths:
        article_url = HABR_URL + article_path
        if '/specials/' not in article_url and not Article.is_in_database(article_url):
            article_urls_to_parse.append(article_url)

    while len(article_urls_to_parse) > 0:
        async with aiohttp.ClientSession() as session:
            urls_fetch_tasks = []
            urls_to_parse_count = min(PARALLEL_REQUESTS, len(article_urls_to_parse))
            for _ in range(urls_to_parse_count):
                urls_fetch_tasks.append(fetch_html(session, article_urls_to_parse.pop()))
            responses_text = await asyncio.gather(*urls_fetch_tasks)

        for article_url, text in responses_text:
            article_page_parser = ArticlePageParser(text)
            logger.info(
                f'New article | Article title: {article_page_parser.article_title} | Article publish date: {article_page_parser.published_at} | Article URL: {article_url} | Author username: {article_page_parser.author_username} | Author URL: {HABR_URL + article_page_parser.author_path}')
            article_data = {
                'hub_id': hub.id,
                'article_title': article_page_parser.article_title,
                'article_text': article_page_parser.article_text,
                'author_url': HABR_URL + article_page_parser.author_path,
                'author_username': article_page_parser.author_username,
                'article_url': article_url,
                'published_at': article_page_parser.published_at
            }
            Article.create(**article_data)

    last_parse_date[hub.id] = datetime.datetime.now()
    logger.info(
        f'Hub {hub.id}: {hub.hub_name} | next parse expected at {datetime.datetime.now() + datetime.timedelta(seconds=hub.poll_interval)}')


async def main():
    logger.info(f'Parser started with PARALLEL_REQUESTS={PARALLEL_REQUESTS}')
    database_sync()
    last_dict_clear_time = datetime.datetime.now()
    while True:

        try:
            hubs_to_parse = Hub.select()
            datetime_now = datetime.datetime.now()
            for hub in hubs_to_parse:
                if hub.id not in last_parse_date or (last_parse_date[hub.id] + datetime.timedelta(
                        seconds=hub.poll_interval) < datetime_now):
                    await parse_hub(hub)

            # периодическая очистка словаря от хабов, удаленных из базы
            if datetime_now > last_dict_clear_time + datetime.timedelta(minutes=10):
                for key in last_parse_date:
                    if key not in {h.id for h in hubs_to_parse}:
                        del last_parse_date[key]
                last_dict_clear_time = datetime_now

        except Exception as err:
            logger.error(err)

        sleep(5)



if __name__ == "__main__":
    asyncio.run(main())
