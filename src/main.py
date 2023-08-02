from webscrapers.g1_webscraper import G1Webscraper
from file_manager import FileManager

manager = FileManager()
g1 = G1Webscraper()
g1.search_for_news_on_first_page()
manager.verify_repeated_data(g1)
g1.extract_news_data()
manager.save_csv(g1.data)