import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "nomsg"
MONGO_COLLECTION = "messages"

COLUMN_ID = "_id"
COLUMN_SENDER = "sender"
COLUMN_CONTENT = "content"
COLUMN_RECEIVER = "receiver"
COLUMN_DATE_TIME = "datetime"


# Get message ID's.
def get_all_messages(receiver_id):
    # Get the client and db.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    messages = db[MONGO_COLLECTION]

    # Do operation.
    message = messages.find({COLUMN_RECEIVER: receiver_id},
                            {COLUMN_ID: 1, COLUMN_SENDER: 1, COLUMN_DATE_TIME: 1, COLUMN_CONTENT: 1})
    client.close()
    return message


# Get message.
def get_message(message_id):
    # Get the client and db.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    messages = db[MONGO_COLLECTION]

    # Do operation.
    message = messages.find_one({COLUMN_ID: ObjectId(message_id)})
    client.close()
    return message


# Delete an entry.
def delete_message(message_id):
    # Get the client, db and collection.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    messages = db[MONGO_COLLECTION]

    # Do operation.
    messages.delete_one({COLUMN_ID: ObjectId(message_id)})
    client.close()


# Delete all entries.
def delete_all_messages(user_name):
    # Get the client, db and collection.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    messages = db[MONGO_COLLECTION]

    # Do operation.
    messages.delete_many({COLUMN_RECEIVER: user_name})
    client.close()


# Add a new entry.
def post_message(sender, receiver, content):
    new_message = {COLUMN_SENDER: sender, COLUMN_CONTENT: content, COLUMN_RECEIVER: receiver,
                   COLUMN_DATE_TIME: datetime.datetime.utcnow()}

    # Get the client and db.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    messages = db[MONGO_COLLECTION]

    # Do operation.
    if new_message is not None:
        message_id = messages.insert_one(new_message).inserted_id
    client.close()
