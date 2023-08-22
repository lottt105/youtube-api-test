from pymongo import MongoClient
import time

MONGO_CRAWLING_URL = "mongodb+srv://naivy:79467946@crawling.fahhu.mongodb.net/"
MONGO_PLAM_URL = "mongodb+srv://naivyplam:GPFFHDNnaivy1!@naivyplam.fc2jf.mongodb.net/"

# crawling db, collection
CRAWLING_DB_NAME = "crawlingdb"
YOUTUBE_TRACK_COLLECTION_NAME = "youtubeTracks"

# plam db, collection
PLAM_DB_NAME = "plam"
PLAM_TRACK_COLLECTION_NAME = "tracks"

client = MongoClient(MONGO_PLAM_URL)
client2 = MongoClient(MONGO_CRAWLING_URL)


def get_datas(
    query,
    fields={},
    db_name=PLAM_DB_NAME,
    collection_name=PLAM_TRACK_COLLECTION_NAME
):
    try:
        db = client[db_name]
        res = db[collection_name].find(query, fields)

        return res
    except Exception as e:
        print("[get_datas] error", e)
        return False
    
def get_data(query, db_name, collection_name):
    try:
        db = client2[db_name]
        res = db[collection_name].find_one(query)
        
        return res
    except Exception as e:
        return False
    

def post_data(data, db_name, collection_name):
    try:
        db = client2[db_name]
        res = db[collection_name].insert_one(data)
        
        return res
    except Exception as e:
        print("[post_data] error", e)
        return False
    
def update_data(query, new_data, db_name, collection_name):
    try:
        db = client2[db_name]
        res = db[collection_name].update_one(query, new_data)
        
        return res
    except Exception as e:
        print("[update_data] error", e)
        return False
    
