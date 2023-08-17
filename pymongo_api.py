from pymongo import MongoClient
import time


MONGO_PLAM_URL = "mongodb+srv://naivyplam:GPFFHDNnaivy1!@naivyplam.fc2jf.mongodb.net/"

# plam db, collection
PLAM_DB_NAME = "plam"
PLAM_TRACK_COLLECTION_NAME = "tracks"

client = MongoClient(MONGO_PLAM_URL)


def get_datas(
    query,
    fields={},
    db_name=PLAM_DB_NAME,
    collection_name=PLAM_TRACK_COLLECTION_NAME,
):
    try:
        db = client[db_name]
        res = db[collection_name].find(query, fields)

        return res
    except Exception as e:
        return False
