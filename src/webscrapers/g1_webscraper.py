from .interfaces.news_webscraper import NewsWebscraper
import numpy as np

class G1Webscraper(NewsWebscraper):
    def __init__(self):
        self.__PAGE_NAME = 'g1'
        self.__BASE_URL = "https://g1.globo.com/"
        self.__NEWS_CONTAINER = {"class": "feed-post-body"}
    
    def extract_first_page_data(self):
        soup = self._get_page(self.__BASE_URL)
        side_section_news = soup.find_all(attrs={"class": "bstn-item-shape"})
        middle_section_news = soup.find_all(attrs={"class": "feed-post-body"})
        extracted_data = []
        for news in middle_section_news:
            data = {
                "titulo": news.h2.string.strip(),
                "url": news.a["href"].strip()
            }
            extracted_data.append(data)
        for news in extracted_data:
            self.__extract_news_data_and_raw_text(news)
        return extracted_data
    
    def __extract_news_data_and_raw_text(self, news_dict):
        news_page = self._get_page(news_dict["url"])
        descricao = news_page.find("h2").get_text().strip() 
        category = news_page.find(attrs = { "class" : "header-editoria--link" }).get_text().strip()
        datetime = news_page.time["datetime"].strip() if news_page.time else np.NAN
        raw_content = news_page.article.get_text().strip()
        news_dict.update({ 
            "data_hora": datetime, 
            "texto_bruto": raw_content, 
            "categoria": category,
            "descricao": descricao
        })


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