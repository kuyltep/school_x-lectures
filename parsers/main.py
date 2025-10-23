from pydantic import BaseModel
import os
import json
from get_urls import get_news_url
from schemas.schemas import News
from parse import parse_news

# @dataclass
# class User(BaseModel):
#   name: str
#   pwd: str
  
  
# user = User(name="vlad", pwd="1234")

# def foo(user: User):
#   print(user.name)
  
# json_data = user.model_dump_json()
# print(json_data)

# print(user.model_validate_json(json_data))

urls = [
    "https://ria.ru/sitemap_article.xml?date_start=20250901&date_end=20250930"
    # "https://ria.ru/sitemap_article.xml?date_start=20250801&date_end=20250831",
    # "https://ria.ru/sitemap_article.xml?date_start=20250701&date_end=20250731",
]

def save_to_file(*, path: str, data: str):
  with open(file=path, mode="w", encoding="utf8") as file:
    file.write(data)

def get_file_name_by_url(*, url: str) -> str:
  
  file_name = url.split("&")[-1].split("=")[-1]
  
  return file_name

def parse_news_urls(*, urls: list[str]) -> None:
  for url in urls:
    news_urls = get_news_url(map_url=url)
    file_name = get_file_name_by_url(url=url)
    
    path = f"./data/{file_name}.json"
    
    json_data = json.dumps([item for item in news_urls])
    
    save_to_file(path=path, data=json_data)
    
    

def parse_all_news():
  path = "./data"
  for json_file in os.listdir(path):
    
    with open(file=f"./data/{json_file}", mode="r", encoding="utf8") as file:
      news_list = json.load(file)

     
    url_list = [news.get("url") for news in news_list]
    
    news_data_list : list[News] = []
    for url in url_list:
      data = parse_news(url=url)
      news_data_list.append(data.model_dump_json())
    
    save_to_file(path=f"./data/news-{json_file}", data=json.dumps(news_data_list))
  
  
parse_news_urls(urls=urls)

parse_all_news()
    
    
      

  
