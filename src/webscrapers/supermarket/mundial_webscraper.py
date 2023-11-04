import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



class MundialWebscraper:
    def __init__(self):
        self.url = 'https://www.supermercadosmundial.com.br/ofertas'

        self.__chrome_options = Options()
        self.__chrome_options.add_argument('no--sandbox')
        self.__chrome_options.add_argument('--headless')
        self.__chrome_options.add_argument('--disable-extensions')
        self.browser = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.__chrome_options
        )
    
    def extract_on_sale_products(self):
        self.browser.get(self.url)
        self.__click_show_more_button()
        on_sale_section = self.browser.find_element(By.XPATH, '//*[@id="stage"]')
        on_sale_products = on_sale_section.find_elements(By.XPATH, '*')
        products = []
        for on_sale_product in on_sale_products:
            name = on_sale_product.find_element(By.CLASS_NAME, 'name-product').text.strip()
            img = on_sale_product.find_element(By.TAG_NAME, 'img').get_attribute('src').strip()
            #TODO: Resolver o problema em acessar esse elemento filho
            raw_price_info = on_sale_product.find_element(By.CLASS_NAME, 'price-product').find_element(By.ID, 'StylePrice').find_element(By.ID, 'porStylePrice').text.strip()
            currency, price, unity = self.__treat_raw_price_data(raw_price_info)
            product = {
                'name': name,
                'img_url': img,
                'currency': currency,
                'price': price,
                'unity': unity
            }
            products.append(product)
        return products

    def __click_show_more_button(self):
        load_more_button = self.browser.find_element(By.ID, 'bnt-carregar')
        while True:
            if load_more_button.value_of_css_property('display') != 'none':
                self.browser.execute_script('arguments[0].click();', load_more_button)
            else:
                break

    def __treat_raw_price_data(self, raw_price: str):
        data = raw_price.split(' ')
        currency = data[0]
        price = float(data[1].replace(',', '.'))
        unity = data[2] if len(data) == 3 else None
        return currency, price, unity