import pymongo
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


# Get message ID's.
def get_message_ids_by_receiver(receiver_id):
    # Get the client and db.
    client = MongoClient('localhost', 27017)
    db = client['nomsg']
    messages = db['messages']

    # Do operation.
    message = messages.find({"receiver_id": receiver_id}, {"_id": 1})
    client.close()
    return message


# Get message.
def get_message(object_id):
    # Get the client and db.
    client = MongoClient('localhost', 27017)
    db = client['nomsg']
    messages = db['messages']

    # Do operation.
    message = messages.find_one({"_id": ObjectId(object_id)})
    client.close()
    return message


# Delete an entry.
def delete_message(object_id):
    # Get the client, db and collection.
    client = MongoClient('localhost', 27017)
    db = client['nomsg']
    messages = db['messages']

    # Do operation.
    messages.delete_one({"_id": ObjectId(object_id)})
    client.close()


# Add a new entry.
def post_message(new_message):
    # Get the client and db.
    client = MongoClient('localhost', 27017)
    db = client['nomsg']
    messages = db['messages']

    # Do operation.
    if new_message is not None:
        message_id = messages.insert_one(new_message).inserted_id
    client.close()
