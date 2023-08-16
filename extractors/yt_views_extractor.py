from requests import get
from bs4 import BeautifulSoup
import json

def yt_views_extractor(yt_url):  
  response = get(yt_url)
  soup = BeautifulSoup(response.text, "html.parser")
  scripts = soup.find_all("script")
  for script in scripts:
    if "var ytInitialPlayerResponse = " in script.text:
      jsonStr = script.text
      jsonStr = jsonStr[jsonStr.index('videoDetails'):].strip()
      
  
  title = jsonStr[jsonStr.index("title")+8:]
  title = title[0:title.index(',')-1]
  
  viewCount = jsonStr[jsonStr.index("viewCount")+12:]
  views = int(viewCount[0:viewCount.index(',')-1])
  
  author = jsonStr[jsonStr.index("author")+9:]
  artist = author[0:author.index(',')-1]

  return [title, artist, views]