from typing import Dict, List, Any
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from exceptions import InvalidUrlException


class GuanabaraWebscraper:
    def __init__(self) -> None:
        self._SOURCE = 'Supermercados Guanabara'
        self._BASE_URL = 'https://www.supermercadosguanabara.com.br'

    def extract_categories_data(self) -> List[Dict[str, str]]:
        webpage = self.__get_webpage(f'{self._BASE_URL}/produtos')
        categories_selection = webpage.find('div', {"class": "item item-menu item-sections"})
        categories_html = categories_selection.findAll('li')
        categories = []
        for category_html in categories_html:
            category_name = category_html.find('a').text
            category_url = category_html.find('a')['href']
            category = {
                "name": category_name,
                "url": self._BASE_URL + category_url
            }
            categories.append(category)
        return categories
    
    def extract_products_data(self, category: str, url: str) -> List[Dict[str, Any]]:
        self.__verify_url(url)
        webpage = self.__get_webpage(url)
        validity_date_text = webpage.find('div', {'class': 'validate'}).find('p').text
        validity_date = self.__extract_date(validity_date_text)
        products_on_page = webpage.findAll('div', {'class': 'col item'})
        products = []
        for product_on_page in products_on_page:
            product_name = product_on_page.find('div', {'class': 'name'}).text.strip()
            product_img = product_on_page.find('div', {'class': 'col image'})['style']
            product_price = product_on_page.find('div', {'class': 'price'}).find('span', {'class':'number'}).text.replace(',','.')
            product = {
                'nome': product_name,
                'preço': float(product_price),
                'categoria': category,
                'origem': self._SOURCE,
                'imagem': self.__extract_url(product_img),
                'data_extração': datetime.now(),
                'data_validade_promoção': validity_date,
            }
            products.append(product)
        return products
    
    def extract_products_data_from_all_categories(self) -> List[Dict[str, Any]]:
        categories = self.extract_categories_data()
        result = []
        for category in categories:
            products = self.extract_products_data(category['name'], category['url'])
            print(f'Foram encontrados {len(products)} para a categoria {category["name"]}')
            result.extend(products)
        print(f'Foram encontrados {len(result)} resultados.')
        return result

    def __get_webpage(self, url: str):
        response = requests.get(url)
        webpage = response.content.decode('utf-8')
        soup = BeautifulSoup(webpage, 'lxml')
        return soup
    
    def __extract_url(self, text: str) -> str:
        pattern = re.compile(r'www.+[a-zA-Z]')
        url_found = pattern.findall(text)
        return url_found[0]
    
    def __extract_date(self, text: str) -> str:
        regex = re.compile(r'[0-9]{2}/[0-9]{2}/[0-9]{4}')
        date = regex.findall(text)
        return date[0]
    
    def __verify_url(self, url: str) -> None:
        if not url.startswith(self._BASE_URL):
            raise InvalidUrlException("Url inválida!")