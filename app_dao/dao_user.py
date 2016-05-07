import pymongo
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


# Add a new entry.
def create_user(user_name):
    # Get the client and db.
    client = MongoClient('localhost', 27017)
    db = client['nomsg']
    users = db['users']

    # Do operation.
    if user_name is not None:
        users.insert_one(user_name).inserted_id
    client.close()
