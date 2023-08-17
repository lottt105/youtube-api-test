import secrets
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_service_name = "youtube"
api_version = "v3"
API_KEY = secrets.YOUTUBE_API_KEY

def yt_api_views(video_ids):
    
    video_ids = ','.join(video_ids)

    # YouTube Data API 클라이언트 생성
    youtube = build(api_service_name, api_version, developerKey=API_KEY)

    try:
        # 비디오 정보 가져오기
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_ids
        )
        video_response = request.execute()
        items = video_response['items']
        
        infos = []
        for i in range(len(items)):
            title = items[i]['snippet']['title'].replace(",", " ")
            artist = items[i]['snippet']['channelTitle'].replace(",", " ")
            views = int(items[i]['statistics']['viewCount'])
            
            infos.append([title, artist, views])
    
        return infos

    except HttpError as e:
        print('에러 발생:', e)