from webscrapers.news.g1_webscraper import G1Webscraper
from webscrapers.supermarket.mundial_webscraper import MundialWebscraper
from file_manager import FileManager

GET_NEWS = False

if GET_NEWS:
    manager = FileManager()
    g1 = G1Webscraper()
    g1.search_for_news_on_first_page()
    manager.verify_repeated_data(g1)
    g1.extract_news_data()
    manager.save_csv(g1.data)

mundial_webscraper = MundialWebscraper()
print(mundial_webscraper.extract_on_sale_products())