from typing import List, Dict, Any
import re

import numpy as np

from webscrapers.base_data import BaseData
from webscrapers.exceptions import InvalidUrlException
from webscrapers.helpers import datetime_convert, treat_string
from .interfaces.news_webscraper import NewsWebscraper
from .news_data import NewsData

class G1Webscraper(NewsWebscraper):
    def __init__(self):
        self.__PAGE_NAME = 'G1'
        self.__BASE_URL = "https://g1.globo.com/"
        self.__raw_data: List[BaseData] = []
        self.__extracted_news_data: List[NewsData] = []
    
    @property
    def source(self):
        return self.__PAGE_NAME
    
    @property
    def raw_data(self) -> List[Dict[str, Any]]:
        return self.__raw_data

    @property
    def data(self) -> List[Dict[str, Any]]:
        return [ data.to_dict() for data in self.__extracted_news_data ]
    
    def remove_data(self, data: BaseData):
        if type(data) == BaseData:
            self.__raw_data.remove(data)

    def search_for_news_on_first_page(self) -> None:
        soup = self._get_page(self.__BASE_URL)
        mais_lidas_section = soup.find_all(attrs={"class": "post-bastian-products__section post-mais-lidas__section"})
        middle_section_news = soup.find_all(attrs={"class": "feed-post-body"})
        for news in middle_section_news:
            try:
                data = BaseData(
                    source  = self.__PAGE_NAME,
                    title   = treat_string(news.h2.string),
                    url     = self.__verify_url(news.a["href"])
                )
                self.__raw_data.append(data)
            except InvalidUrlException:
                print(f"Url inválida para: '{data.title}'")
        print(f"Foram encontradas {len(self.__raw_data)} notícias na primeira página de {self.__PAGE_NAME}.")

    def __verify_url(self, url: str) -> None:
        if url.startswith(self.__BASE_URL):
            return url
        raise InvalidUrlException("Url inválida!")

    def extract_news_data(self) -> None:
        for data in self.__raw_data:
            try:
                news_data = self.__extract_infos_and_raw_text(data)
                self.__extracted_news_data.append(news_data)
            except:
                print(f"Ocorreu um erro extraindo mais informações da notícia com título: '{data.title}'")
        self.__raw_data.clear()

    def __extract_infos_and_raw_text(self, data: BaseData) -> None:
        news_page = self._get_page(data.url)
        description = treat_string(news_page.find("h2").get_text().strip())
        category = news_page.find(attrs = { "class" : "header-editoria--link" }).get_text().strip()
        datetime = datetime_convert(news_page.time["datetime"].strip()) if news_page.time else np.NAN
        raw_text = self.__remove_figure_captions(treat_string(news_page.article.get_text().strip()))
        return NewsData.fromBaseData(
            base_data   = data,
            description = description,
            category    = category,
            raw_text    = raw_text,
            datetime    = datetime
        )

    def __remove_figure_captions(self, text: str) -> str:
        search_pattern = re.compile("[\d][\s]de[\s][\d][\s].*[—][\s]Foto[:]")
        return re.sub(search_pattern, "", text)

    def extract_editorial_page_data(self):
        soup = self._get_page(self.__BASE_URL)
        news = soup.find_all(attrs=self.__NEWS_CONTAINER)
        extracted_data = []
        for new in news:
            data = {
                "titulo":  new.h2.string,
                "descricao": new.p.string,
                "url": new.a["href"]
            }
        extracted_data.append(data)
        return extracted_data