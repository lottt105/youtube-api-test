import time
import copy
from datetime import date
from youtube_data_api import fetch_youtube_data
from plam_api import fetch_plam_premium_artist_list
from bson.objectid import ObjectId
from pymongo_api import (
    get_datas,
    get_data,
    post_data,
    update_data,
    CRAWLING_DB_NAME,
    PLAM_DB_NAME,
    PLAM_TRACK_COLLECTION_NAME,
    YOUTUBE_TRACK_COLLECTION_NAME,
    YOUTUBE_ERROR_COLLECTION_NAME
)

# 플램에서 해당 아티스트 트랙 정보 받아옴
def fetch_track_list():
  plam_premium_artist_list = fetch_plam_premium_artist_list()
  total_tracks = {}
  
  print("artist_length", len(plam_premium_artist_list))
  for artist in plam_premium_artist_list[0 : len(plam_premium_artist_list)]:
    
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
    
    for track in _tracks[0:len(_tracks)]:
      
      youtube_music_url = track["youtubeMusicUrl"]
      
      if youtube_music_url:
        video_id = youtube_music_url[youtube_music_url.find("v=") + 2:]
        end_index = len(video_id) if video_id.find("&") == -1 else video_id.find("&")
        total_tracks[video_id[:end_index]] = copy.deepcopy(track)
  
  return total_tracks

def update_track_data():
  start_time = time.time()   
        
  today = date.today().strftime("%Y-%m-%d")
  success_youtube_music_infos = []
  wrong_youtube_music_infos = []

  # 유튜브에서 트랙별 데이터 받아옴
  total_tracks = fetch_track_list()
  repeat_count = (len(total_tracks) // 50) + 1

  for i in range(repeat_count):
    video_ids_50 = list(total_tracks.keys())[i*50:(i+1)*50]
    youtube_music_infos_50 = fetch_youtube_data(video_ids_50)
    
    # api 요청으로 못 받아온 데이터 모아둠
    infos_video_ids = list(youtube_music_infos_50.keys())
    for v_id in video_ids_50:
      if v_id not in infos_video_ids:
        wrong_youtube_music_infos.append(total_tracks[v_id])
      else:
        views = youtube_music_infos_50[v_id]["views"]
        likes = youtube_music_infos_50[v_id]["likes"]
      
        get_query = {"_id": total_tracks[v_id]["_id"]}
        exsiting_data = get_data(
          get_query, CRAWLING_DB_NAME, YOUTUBE_TRACK_COLLECTION_NAME
        )
        # db에 없는 트랙이면, 초기값 넣어줌
        if not exsiting_data:
          total_tracks[v_id]["youtubeMusicId"] = v_id
          total_tracks[v_id]["youtubeMusicViews"] = {
            "total": 0,
            "daily": []
          }
          total_tracks[v_id]["youtubeMusicLikes"] = {
            "total": 0,
            "daily": []
          }
          res = post_data(
            total_tracks[v_id], CRAWLING_DB_NAME, YOUTUBE_TRACK_COLLECTION_NAME
          )
          if res:
            post_check += 1
            exsiting_data = get_data(
              get_query, CRAWLING_DB_NAME, YOUTUBE_TRACK_COLLECTION_NAME
            )
  
        # 오늘 데이터 체크
        isExistDatePopularity = False
        updateIndexPopularity = None
        
        for i, e in enumerate(exsiting_data["youtubeMusicViews"]["daily"]):
          if e["date"] == today:
            isExistDatePopularity = True
            updateIndexPopularity = i
            
        today_views = {
          "count": views,
          "date": today,
          "createdAt": time.time()
        }
        today_likes = {
          "count": likes,
          "date": today,
          "createdAt": time.time()
        }
        update_query = {"_id": total_tracks[v_id]["_id"]} 
        update_views_params = {}
        update_likes_params = {}
        
        if isExistDatePopularity:
          update_views_params = {
            "$set": {
              "youtubeMusicViews.total": views,
              f"youtubeMusicViews.daily.{updateIndexPopularity}": today_views
            }
          }
          update_likes_params = {
            "$set": {
              "youtubeMusicLikes.total": likes,
              f"youtubeMusicLikes.daily.{updateIndexPopularity}": today_likes
            },
          }
        else:
          update_views_params = {
            "$set": {
              "youtubeMusicViews.total": views
            },
            "$push": {"youtubeMusicViews.daily": today_views}
          }
          update_likes_params = {
            "$set": {
              "youtubeMusicLikes.total": likes
            },
            "$push": {"youtubeMusicLikes.daily": today_views}
          }
        
        # db에 오늘 데이터 추가
        update_views_res = update_data(
          query=update_query,
          new_data=update_views_params,
          db_name=CRAWLING_DB_NAME,
          collection_name=YOUTUBE_TRACK_COLLECTION_NAME
        )
        
        update_likes_res = update_data(
          query=update_query,
          new_data=update_likes_params,
          db_name=CRAWLING_DB_NAME,
          collection_name=YOUTUBE_TRACK_COLLECTION_NAME
        )
        
        if update_views_res and update_likes_res:
          success_youtube_music_infos.append(total_tracks[v_id])
  
  wrong_infos = {
    today: wrong_youtube_music_infos 
  }
  res = post_data(wrong_infos, CRAWLING_DB_NAME, YOUTUBE_ERROR_COLLECTION_NAME) 
       
  duration = time.time() - start_time
  print("소요시간:", duration,"초") 
     
update_track_data()