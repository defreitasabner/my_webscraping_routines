from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

from webscrapers.base_data import BaseData
from webscrapers.exceptions import InvalidUrlException
from webscrapers.news_data import NewsData

class NewsWebscraper:
    def __init__(self, page_name: str, base_url: str):
        self._PAGE_NAME = page_name
        self._BASE_URL = base_url
        self._raw_data: List[BaseData] = []
        self._extracted_news_data: List[NewsData] = []
    
    @property
    def source(self):
        return self._PAGE_NAME
    
    @property
    def raw_data(self) -> List[Dict[str, Any]]:
        return self._raw_data

    @property
    def data(self) -> List[Dict[str, Any]]:
        return [ data.to_dict() for data in self._extracted_news_data ]

    def remove_data(self, data: BaseData):
        if type(data) == BaseData:
            self._raw_data.remove(data)

    def _get_page(self, url):
        response = requests.get(url)
        webpage = response.content.decode("utf-8")
        return BeautifulSoup(webpage, 'lxml')

    def search_for_news_on_first_page(self):
        raise NotImplementedError()
    
    def _verify_url(self, url: str) -> None:
        if url.startswith(self._BASE_URL):
            return url
        raise InvalidUrlException("Url inválida!")
    
    def extract_news_data(self) -> None:
        for data in self._raw_data:
            try:
                news_data = self._extract_infos_and_raw_text(data)
                self._extracted_news_data.append(news_data)
            except:
                print(f"Ocorreu um erro extraindo mais informações da notícia com título: '{data.title}'")
        self._raw_data.clear()

    def _extract_infos_and_raw_text(self, data: BaseData) -> None:
        raise NotImplementedError()