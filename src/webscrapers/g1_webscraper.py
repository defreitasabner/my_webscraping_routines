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
        super().__init__(page_name = 'G1', base_url = "https://g1.globo.com/")

    def search_for_news_on_first_page(self) -> None:
        soup = self._get_page(self._BASE_URL)
        mais_lidas_section = soup.find_all(attrs={"class": "post-bastian-products__section post-mais-lidas__section"})
        middle_section_news = soup.find_all(attrs={"class": "feed-post-body"})
        for news in middle_section_news:
            try:
                data = BaseData(
                    source  = self._PAGE_NAME,
                    title   = treat_string(news.h2.string),
                    url     = self._verify_url(news.a["href"])
                )
                self._raw_data.append(data)
            except InvalidUrlException:
                print(f"Url inválida para: '{data.title}'")
        print(f"Foram encontradas {len(self._raw_data)} notícias na primeira página de {self._PAGE_NAME}.")

    def _extract_infos_and_raw_text(self, data: BaseData) -> None:
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