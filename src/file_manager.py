from typing import List, Dict, Any
import pandas as pd
import os

from webscrapers.g1_webscraper import G1Webscraper

class FileManager:
    def __init__(self):
        self.__NEWS_DATA = os.path.join("src", "data", "news.csv")

        self.__news_df = self.read_csv(self.__NEWS_DATA)
    
    def verify_repeated_data(self, news_webscraper: G1Webscraper):
        if type(self.__news_df) is pd.DataFrame:
            filtered_dataframe = self.__news_df.query(f"origem == '{news_webscraper.source}'")
            for data in news_webscraper.raw_data:
                if data.url in filtered_dataframe["url"].unique():
                    print(f"- A notícia com título '{data.title}' foi removida pois já existe no dataset.")
                    news_webscraper.remove_data(data)

    def read_csv(self, path: str) -> pd.DataFrame:
        try:
            if os.path.exists(path):
                return pd.read_csv(path, sep=";")
            else:
                return None
        except:
            print(f"Ocorreu um erro enquanto abria o dataset.")

    def save_csv(self, data: List[Dict[str, Any]]) -> None:
        new_dataframe = pd.DataFrame.from_records(data)
        print(new_dataframe.info())
        new_dataframe["titulo"] = new_dataframe["titulo"].astype("string")
        new_dataframe["url"] = new_dataframe["url"].astype("string")
        new_dataframe["descricao"] = new_dataframe["descricao"].astype("string")
        new_dataframe["texto_bruto"] = new_dataframe["texto_bruto"].astype("string")
        new_dataframe["origem"] = new_dataframe["origem"].astype("string")
        new_dataframe["categoria"] = new_dataframe["categoria"].astype("category")
        if os.path.exists(self.__NEWS_DATA):
            existing_dataframe = pd.read_csv(self.__NEWS_DATA)
            dataframe = pd.concat([existing_dataframe, new_dataframe])
            dataframe.drop_duplicates(subset=["titulo", "url"], inplace = True)
            dataframe.to_csv(self.__NEWS_DATA, index=False)
        else:
            new_dataframe.to_csv(self.__NEWS_DATA, index=False)