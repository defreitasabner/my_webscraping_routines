from typing import List, Dict, Any
import pandas as pd
import os

class FileManager:
    def __init__(self):
        self.__NEWS_DATA = os.path.join("src", "data", "news.csv")
    
    def save_csv(self, data: List[Dict[str, Any]]) -> None:
        try:
            new_dataframe = pd.DataFrame.from_records(data)
            if os.path.exists(self.__NEWS_DATA):
                existing_dataframe = pd.read_csv(self.__NEWS_DATA)
                dataframe = pd.concat([existing_dataframe, new_dataframe])
                dataframe.drop_duplicates(subset=["titulo", "url"], inplace = True)
                dataframe.to_csv(self.__NEWS_DATA, index=False)
            else:
                new_dataframe.to_csv(self.__NEWS_DATA, index=False)
        except Exception as error:
            print(f"Ocorreu um erro!")