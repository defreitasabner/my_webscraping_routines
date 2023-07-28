from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class NewsWebscraper(ABC):

    @abstractmethod
    def extract_first_page_data(self):
        pass

    def _get_page(self, url):
        response = requests.get(url)
        webpage = response.content.decode("utf-8")
        return BeautifulSoup(webpage, 'lxml')