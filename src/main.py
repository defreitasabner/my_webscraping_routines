from webscrapers.g1_webscraper import G1Webscraper
from file_manager import FileManager

import pandas as pd

g1 = G1Webscraper()
data = g1.extract_first_page_data()

manager = FileManager()
manager.save_csv(data)
print(pd.read_csv("src/data/news.csv"))
