from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class NewsWebscraper(ABC):

    @abstractmethod
    def search_for_news_on_first_page(self):
        pass

    def _get_page(self, url):
        response = requests.get(url)
        webpage = response.content.decode("utf-8")
        return BeautifulSoup(webpage, 'lxml')