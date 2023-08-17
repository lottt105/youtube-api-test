from datetime import datetime
from yt_api_views import yt_api_views
from plam_api import fetch_plam_premium_artist_list

from bson.objectid import ObjectId
from pymongo_api import (
    get_datas,
    PLAM_DB_NAME,
    PLAM_TRACK_COLLECTION_NAME,
)

# 플램에서 해당 아티스트 트랙 정보 받아옴
plam_premium_artist_list = fetch_plam_premium_artist_list()
totalTracks = []
video_ids = []

youtube_music_infos = []

for artist_index, artist in enumerate(
    plam_premium_artist_list[0 : len(plam_premium_artist_list)]):
  
  artist_name = artist["name"]
  
  get_query = {
      "releaseArtistIdList": {"$in": [ObjectId(artist["plamArtistId"])]},
      "deletedAt": None,
  }
  get_fields = {
      "title": 1,
      "releaseArtistIdList": 1,
      "artistInfo": 1,
      "youtubeMusicUrl": 1,
  }

  tracks = get_datas(
      query=get_query,
      fields=get_fields,
      db_name=PLAM_DB_NAME,
      collection_name=PLAM_TRACK_COLLECTION_NAME,
  )
  
  _tracks = list(tracks)
  for track_index, track in enumerate(
    _tracks[0:len(_tracks)]):
    
    youtube_music_url = track["youtubeMusicUrl"]
    if youtube_music_url:
      totalTracks.append(track)
      
      video_id = youtube_music_url[youtube_music_url.find("v=") + 2:]
      video_ids.append(video_id[:video_id.find("&")])
          
# 유튜브에서 정보 트랙별 정보 받아옴
repeat_count = (len(video_ids) // 50) + 1
for i in range(repeat_count):
  youtube_music_infos_50 = yt_api_views(video_ids[i*50:(i+1)*50])
  youtube_music_infos = youtube_music_infos + youtube_music_infos_50

file = open(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}.csv", "w", encoding='utf-8')
file.write("title,artist,views\n")
for youtube_music_info in youtube_music_infos:
  file.write(f"{youtube_music_info[0]},{youtube_music_info[1]},{youtube_music_info[2]}\n")
file.close()