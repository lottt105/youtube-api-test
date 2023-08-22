import secrets
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_service_name = "youtube"
api_version = "v3"
API_KEY = secrets.YOUTUBE_API_KEY

def fetch_youtube_data(video_ids):
    video_ids = ','.join(video_ids)

    # YouTube Data API 클라이언트 생성
    youtube = build(api_service_name, api_version, developerKey=API_KEY)

    try:
        # api에서 video_ids 정보 가져오기
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_ids
        )
        video_response = request.execute()
        items = video_response['items']
        
        infos = {}
        for i in range(len(items)):
            v_id = items[i]["id"]
            views = int(items[i]['statistics']['viewCount'])
            likes = int(items[i]['statistics']['likeCount'])
            
            infos[v_id] = {
                "views": views, 
                "likes": likes
            }
            
        return infos
            
    except Exception as e:
        print('[fetch_youtube_data]에러 발생:', e)
        