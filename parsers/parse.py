import requests
from bs4 import BeautifulSoup
from schemas.schemas import News

# url = "https://ria.ru/20251014/minobrnauki-2048150182.html"

def parse_news(*, url: str) -> News:
  res = requests.get(url)

  print(res.status_code)
  if res.ok:
    
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("div", {"class": "article__title"}).text
    
    text = soup.find("div", {"class": "article__body"}).text
    
    date = soup.find("div", {"class": "article__info-date"}).text
    
    return News(title=title, text=text, date=date)