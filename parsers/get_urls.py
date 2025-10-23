import requests
import json
from schemas.schemas import NewsUrl
import xmltodict

# url = "https://ria.ru/sitemap_article.xml?date_start=20251001&date_end=20251016"

def get_news_url(*, map_url: str) -> list[NewsUrl]:
  
  
  xml = requests.get(map_url)
  xml_text = xml.text
  
  
  xml_dict = xmltodict.parse(xml_input=xml_text).get("urlset").get("url")

    
  news_list: list[NewsUrl] = [NewsUrl(url=item.get("loc"), lastmod=item.get("lastmod")) for item in xml_dict]
  
  return news_list
