from typing import List, Dict, Any
import pandas as pd
import os

from webscrapers.news.g1_webscraper import G1Webscraper

class FileManager:
    def __init__(self):
        self.__RAW_NEWS_DATA = os.path.join("data", "raw_news.csv")
        self.__RAW_SUPERMARKET_DATA = os.path.join("data", "raw_supermarket.csv")

        self.__news_df = self.read_csv(self.__RAW_NEWS_DATA)
    
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
                return pd.read_csv(path)
            else:
                return None
        except:
            print(f"Ocorreu um erro enquanto abria o dataset.")

    def save_news_csv(self, data: List[Dict[str, Any]]) -> None:
        new_dataframe = pd.DataFrame.from_records(data)
        new_dataframe["titulo"] = new_dataframe["titulo"].astype("string")
        new_dataframe["url"] = new_dataframe["url"].astype("string")
        new_dataframe["descricao"] = new_dataframe["descricao"].astype("string")
        new_dataframe["texto_bruto"] = new_dataframe["texto_bruto"].astype("string")
        new_dataframe["origem"] = new_dataframe["origem"].astype("string")
        new_dataframe["categoria"] = new_dataframe["categoria"].astype("category")
        if os.path.exists(self.__RAW_NEWS_DATA):
            existing_dataframe = pd.read_csv(self.__RAW_NEWS_DATA)
            dataframe = pd.concat([existing_dataframe, new_dataframe])
            dataframe.drop_duplicates(subset=["titulo", "url"], inplace = True)
            dataframe.to_csv(self.__RAW_NEWS_DATA, index=False)
        else:
            new_dataframe.to_csv(self.__RAW_NEWS_DATA, index=False)

    def save_supermarket_csv(self, data: List[Dict[str, Any]]) -> None:
        new_dataframe = pd.DataFrame.from_records(data)
        new_dataframe["nome"] = new_dataframe["nome"].astype("string")
        new_dataframe["preço"] = new_dataframe["preço"].astype("float64")
        new_dataframe["categoria"] = new_dataframe["categoria"].astype("category")
        new_dataframe["origem"] = new_dataframe["origem"].astype("string")
        new_dataframe['imagem'] = new_dataframe['imagem'].astype('string')
        new_dataframe["data_extração"] = new_dataframe["data_extração"].astype("datetime64[ns]")
        new_dataframe["data_validade_promoção"] = new_dataframe["data_validade_promoção"].astype("string")
        if os.path.exists(self.__RAW_SUPERMARKET_DATA):
            existing_dataframe = pd.read_csv(self.__RAW_SUPERMARKET_DATA)
            dataframe = pd.concat([existing_dataframe, new_dataframe])
            dataframe.drop_duplicates(subset=['nome', 'origem', 'preço', 'data_validade_promoção'], keep = 'first', inplace = True)
            dataframe.to_csv(self.__RAW_SUPERMARKET_DATA, index=False)
        else:
            new_dataframe.to_csv(self.__RAW_SUPERMARKET_DATA, index=False)