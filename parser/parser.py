from bs4 import BeautifulSoup


class ArticlePageParser:
    def __init__(self, html_source):
        self.soup = BeautifulSoup(html_source, features='html.parser')
        self.parse()

    def parse(self):
        self.article_title = self.soup.find('h1').get_text().strip()
        self.article_text = self.soup.find('div', id='post-content-body').get_text().strip()
        self.author_path = self.soup.find('a', class_='tm-user-info__username').get('href').strip()
        self.author_username = self.soup.find('a', class_='tm-user-info__username').get_text().strip()
        self.published_at = self.soup.find('span', class_='tm-article-datetime-published').time.get('datetime').strip()


class HubPageParser:
    def __init__(self, html_source):
        self.soup = BeautifulSoup(html_source, features='html.parser')

        self.parse()

    def parse(self):
        self.article_paths = [a.get('href') for a in self.soup.find_all('a', {'data-article-link': 'true'})]
        self.hub_title = self.soup.find('h1').get_text().strip()
