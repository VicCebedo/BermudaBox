import pyotp
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "nomsg"
MONGO_COLLECTION = "users"

COLUMN_ID = "_id"
COLUMN_USER_NAME = "user_name"
COLUMN_TOTP_SECRET = "totp_secret"


# Add a new entry.
def create_user(user_name):
    # Get the client and db.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    users = db[MONGO_COLLECTION]

    # Do operation.
    if user_name is not None:
        totp_secret = pyotp.random_base32()
        user = {COLUMN_USER_NAME: user_name, COLUMN_TOTP_SECRET: totp_secret}
        users.insert_one(user).inserted_id
    client.close()


# Get secret.
def get_user_secret(user_name):
    # Get the client and db.
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    users = db[MONGO_COLLECTION]

    # Get the user's secret.
    totp_secret = users.find_one({COLUMN_USER_NAME: user_name}, {COLUMN_TOTP_SECRET: 1, COLUMN_ID: 0})

    # Return blank if null.
    # Otherwise, normal behaviour.
    if totp_secret is None:
        return ""
    user_secret = totp_secret[COLUMN_TOTP_SECRET]
    return user_secret
