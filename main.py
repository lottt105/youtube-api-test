from datetime import datetime
from extractors.yt_views_extractor import yt_views_extractor
from yt_api_views import yt_api_views

yt_urls = [
    "https://music.youtube.com/watch?v=0c7zGU2C2mM",
    "https://music.youtube.com/watch?v=AMg1locCoN0",
    "https://music.youtube.com/watch?v=-9fC6oDFl5k",
    "https://music.youtube.com/watch?v=58IEh6YkuzQ",
    "https://music.youtube.com/watch?v=fbmStVcCL8s",
    "https://music.youtube.com/watch?v=Y4JQokTmBTA",
    "https://music.youtube.com/watch?v=ZnR0JiQGxRE",
    "https://music.youtube.com/watch?v=j1uXcHwLhHM",
    "https://music.youtube.com/watch?v=XbaSYBK5Nc0",
    "https://music.youtube.com/watch?v=A1tZgPAcpjE"
  ]

# youtube data api 사용
video_ids = []
for yt_url in yt_urls:
  video_ids.append(yt_url[yt_url.find("v=") + 2 :])
infos = yt_api_views(video_ids)

file = open(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}.csv", "w", encoding='utf-8')
file.write("title,artist,views\n")
for info in infos:
  file.write(f"{info[0]},{info[1]},{info[2]}\n")
file.close()