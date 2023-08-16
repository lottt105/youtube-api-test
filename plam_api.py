import requests

def fetch_plam_premium_artist_list():
    _URL = "https://api-v1.plam.kr/artist/all/premium"
    _headers = {"Authorization": "jwt"}
    artist_list = []

    try:
        res = requests.get(_URL, headers=_headers)
        plam_artist_list = res.json()["data"]["artistList"]

        for artist in plam_artist_list:
            # 플램은 가계정이라 제외
            if artist["uniqueName"] == "plam":
                continue
                
            artist_info = {
                "plamArtistId": artist["_id"],
                "youtubeMusicUrl": artist["youtubeMusicUrl"],
                "userId": artist["userId"],
                "uniqueName": artist["uniqueName"],
                "name": artist["name"],
            }
            
            if artist_info["youtubeMusicUrl"]:
                artist_list.append(artist_info)

        return artist_list

    except HttpError as e:
        print('에러 발생:', e)
