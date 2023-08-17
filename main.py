from datetime import datetime
from yt_api_views import yt_api_views
from plam_api import fetch_plam_premium_artist_list

from bson.objectid import ObjectId
from pymongo_api import (
    get_datas,
    PLAM_DB_NAME,
    PLAM_TRACK_COLLECTION_NAME,
)
import time

start = time.time()

# 플램에서 해당 아티스트 트랙 정보 받아옴
def fetch_track_list():
  plam_premium_artist_list = fetch_plam_premium_artist_list()
  totalTracks = []
  video_ids = {}

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
      
      track_id = track["_id"]
      title = track["title"]
      artist_name = track["artistInfo"]["name"]
      artist_id = track["artistInfo"]["_id"]
      youtube_music_url = track["youtubeMusicUrl"]
      
      if youtube_music_url:
        totalTracks.append(track)
        
        video_id = youtube_music_url[youtube_music_url.find("v=") + 2:]
        end_index = len(video_id) if video_id.find("&") == -1 else video_id.find("&")
        video_ids[video_id[:end_index]] = {
          "track_id" : track_id,
          "title" : title,
          "artist_name" : artist_name,
          "artist_id" : artist_id,
          "youtubeMusicUrl" : youtube_music_url,
          "video_id" : video_id[:end_index]
        }
  return video_ids
          
# 유튜브에서 트랙별 데이터 받아옴
youtube_music_infos = []
failed_youtube_music_infos = []

video_ids = fetch_track_list()
print(len(video_ids))
repeat_count = (len(video_ids) // 50) + 1
for i in range(repeat_count):
  video_ids_50 = list(video_ids.keys())[i*50:(i+1)*50]
  youtube_music_infos_50 = yt_api_views(video_ids_50)
  
  # api 요청으로 못 받아온 데이터 모아둠
  if len(youtube_music_infos_50) < 50:
    infos_video_ids = [x[4] for x in youtube_music_infos_50]
    for v in video_ids_50:
      if v not in infos_video_ids:
        failed_youtube_music_infos.append(video_ids[v])
  
  youtube_music_infos = youtube_music_infos + youtube_music_infos_50

end = time.time()
print(end-start)

# 파일에 저장, 나중에 수정
file = open(f"{datetime.today().year}{datetime.today().month}{datetime.today().day}.csv", "w", encoding='utf-8')
file.write("title,artist,views,likes\n")
for youtube_music_info in youtube_music_infos:
  file.write(f"{youtube_music_info[0]},{youtube_music_info[1]},{youtube_music_info[2]},{youtube_music_info[3]}\n")
file.close()