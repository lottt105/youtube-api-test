from datetime import datetime
from yt_api_views import yt_api_views
from plam_api import fetch_plam_premium_artist_list

artist_list = fetch_plam_premium_artist_list()
print(artist_list)

"""
# youtube data api 사용
video_ids = []
for yt_url in yt_urls:
  video_ids.append(yt_url[yt_url.find("v=") + 2 :])
infos = yt_api_views(video_ids)
print(infos)
file = open(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}.csv", "w", encoding='utf-8')
file.write("title,artist,views\n")
for info in infos:
  file.write(f"{info[0]},{info[1]},{info[2]}\n")
file.close()
"""