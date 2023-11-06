from typing import Dict, List
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class GuanabaraWebscraper:
    def __init__(self) -> None:
        self._source = 'Supermercados Guanabara'

    def extract_categories_data(self) -> List[Dict[str, str]]:
        webpage = self.__get_webpage('https://www.supermercadosguanabara.com.br/produtos')
        categories_selection = webpage.find('div', {"class": "item item-menu item-sections"})
        categories_html = categories_selection.findAll('li')
        categories = []
        for category_html in categories_html:
            category_name = category_html.find('a').text
            category_url = category_html.find('a')['href']
            category = {
                "name": category_name,
                "url": 'https://www.supermercadosguanabara.com.br' + category_url
            }
            categories.append(category)
        return categories
    
    def extract_products_data(self, category: str, url: str) -> List[Dict[str, str]]:
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
                'origem': self._source,
                'imagem': self.__extract_url(product_img),
                'data_extração': datetime.now(),
                'data_validade_promoção': datetime.strptime(validity_date, '%d/%m/%Y'),
            }
            products.append(product)
        return products
    
    def extract_products_data_from_all_categories(self):
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
    
    def __extract_url(self, text):
        pattern = re.compile(r'www.+[a-zA-Z]')
        url_found = pattern.findall(text)
        return url_found[0]
    
    def __extract_date(self, text: str) -> str:
        regex = re.compile(r'[0-9]{2}/[0-9]{2}/[0-9]{4}')
        date = regex.findall(text)
        return date[0]