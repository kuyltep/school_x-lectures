from pydantic import BaseModel, AnyUrl
from datetime import datetime

class NewsUrl(BaseModel):
  url: AnyUrl
  lastmod: datetime
  

class News(BaseModel):
  title: str
  text: str
  date: datetime