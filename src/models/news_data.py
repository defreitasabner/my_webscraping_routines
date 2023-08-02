from models.base_data import BaseData

class NewsData:
    def __init__(
        self, 
        title: str, 
        url: str, 
        source: str, 
        description: str,
        datetime: str,
        raw_text: str,
        category: str
        ) -> None:
        self.source = source
        self.title = title
        self.url = url
        self.description: str = description
        self.datetime: str = datetime
        self.raw_text: str = raw_text
        self.category: str = category

    def to_dict(self):
        news_data = {
            "titulo": self.title,
            "url": self.url,
            "descricao": self.description,
            "data_hora": self.datetime,
            "texto_bruto": self.raw_text,
            "categoria": self.category,
            "origem": self.source
        }
        return news_data
    
    @staticmethod
    def fromBaseData(
        base_data: BaseData, 
        description: str, 
        category: str, 
        raw_text: str, 
        datetime: str
    ):
        return NewsData(
            source      = base_data.source,
            title       = base_data.title,
            url         = base_data.url,
            description = description,
            category    = category,
            raw_text    = raw_text,
            datetime    = datetime
        )
