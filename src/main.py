from webscrapers.news.g1_webscraper import G1Webscraper
from webscrapers.supermarket.mundial_webscraper import MundialWebscraper
from webscrapers.supermarket.guanabara_webscraper import GuanabaraWebscraper
from file_manager import FileManager

GET_NEWS = False
GET_SUPERMARKET = True

manager = FileManager()

if GET_NEWS:
    g1 = G1Webscraper()
    g1.search_for_news_on_first_page()
    manager.verify_repeated_data(g1)
    g1.extract_news_data()
    manager.save_news_csv(g1.data)

elif GET_SUPERMARKET:
    guanabara = GuanabaraWebscraper()
    data = guanabara.extract_products_data_from_all_categories()
    manager.save_supermarket_csv(data)