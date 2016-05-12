import requests
import validator as validator
import app_dao.dao_message as dao_message
import app_dao.dao_user as dao_user
from bson import json_util
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ERROR_INVALID_2FA = "Error: Invalid 2FA."
ERROR_N0_USER = "Error: User does not exist: "
ERROR_USER_EXISTS = "Error: User already exists."
ERROR_INVALID_RECAPTCHA = "Error: reCAPTCHA not valid."
ERROR_VALIDATION = "Error: Input not valid."
NOTE_INBOX_EMPTY = "Note: Inbox is empty."

SUCCESS_MESSAGE_SENT = "Message sent."
SUCCESS_USER_CREATED = "User created. Secret Key: "
SUCCESS_MESSAGE_DELETE = "Deleted message."
SUCCESS_MESSAGE_DELETE_ALL = "Deleted all messages: "


# Get the inbox.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['GET'])
def get_all_messages(user_name, totp_token):
    # Input validation.
    if not (validator.user_name_valid(user_name)
            and validator.totp_valid(totp_token)):
        return ERROR_VALIDATION

    # Check if user exists.
    if not dao_user.user_exists(user_name):
        return ERROR_N0_USER + user_name

    # Check 2FA.
    if not validator.alive_token(user_name, totp_token):
        return ERROR_INVALID_2FA

    # Fetch the ID's.
    messages = dao_message.get_all_messages(user_name)
    if (messages.count() > 0):
        return json_util.dumps(messages)
    return NOTE_INBOX_EMPTY


# Verify recaptcha then create user.
@app.route('/user/<user_name>/', methods=['POST'])
def create_user(user_name):
    # Input validation.
    if not validator.user_name_valid(user_name):
        return ERROR_VALIDATION

    # TODO Find a better way of extracting data from request.
    secret = request.json[0].get('secret')
    response = request.json[1].get('response')

    # Verify in google.
    google_response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                    data={'secret': secret, 'response': response})
    success = json_util.loads(google_response.text)['success']

    # If success, create a new user.
    if success:
        # Check if already exists.
        if dao_user.user_exists(user_name):
            return ERROR_USER_EXISTS

        totp_secret = dao_user.create_user(user_name)
        return SUCCESS_USER_CREATED + totp_secret

    return ERROR_INVALID_RECAPTCHA


# Delete entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['DELETE'])
def delete_message(user_name, totp_token, message_id):
    # Input validation.
    if not (validator.user_name_valid(user_name)
            and validator.totp_valid(totp_token)
            and validator.message_id_valid(message_id)):
        return ERROR_VALIDATION

    # Check token life.
    if not validator.alive_token(user_name, totp_token):
        return ERROR_INVALID_2FA

    # Do operation and return.
    dao_message.delete_message(message_id)
    return SUCCESS_MESSAGE_DELETE


# Delete all entries.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['DELETE'])
def delete_all_messages(user_name, totp_token):
    # Input validation.
    if not (validator.user_name_valid(user_name)
            and validator.totp_valid(totp_token)):
        return ERROR_VALIDATION

    # Check if token is alive.
    if not validator.alive_token(user_name, totp_token):
        return ERROR_INVALID_2FA

    # Do operation then return.
    dao_message.delete_all_messages(user_name)
    return SUCCESS_MESSAGE_DELETE_ALL + user_name


# Add entry.
@app.route('/user/<receiver_user_name>/sender/<sender_user_name>/2fa/<totp_token>/message/', methods=['POST'])
def post_message(receiver_user_name, sender_user_name, totp_token):
    # Input validation.
    content = json_util.Binary.decode(request.data)
    if not (validator.user_name_valid(receiver_user_name)
            and validator.user_name_valid(sender_user_name)
            and validator.totp_valid(totp_token)
            and validator.content_valid(content)):
        return ERROR_VALIDATION

    # Check if receiver exists.
    if not dao_user.user_exists(receiver_user_name):
        return ERROR_N0_USER + receiver_user_name

    # Check if sender exists.
    if not dao_user.user_exists(sender_user_name):
        return ERROR_N0_USER + sender_user_name

    # Check if valid 2FA.
    if not validator.alive_token(sender_user_name, totp_token):
        return ERROR_INVALID_2FA

    # Do operation and return.
    dao_message.post_message(sender_user_name, receiver_user_name, content)
    return SUCCESS_MESSAGE_SENT


# Add entry as anonymous.
# @app.route('/user/<receiver_user_name>/sender/anon/message/', methods=['POST'])
# def post_message_anon(receiver_user_name):
#     # Check if receiver exists.
#     if not dao_user.user_exists(receiver_user_name):
#         return ERROR_N0_USER
#
#     # Do operation.
#     content = request.data
#     dao_message.post_message("anon", receiver_user_name, content)
#     return SUCCESS_MESSAGE_SENT


# Get entry.
# @app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['GET'])
# def get_message(user_name, totp_token, message_id):
#     # Input validation.
#     if not (validator.user_name_valid(user_name)
#             and validator.totp_valid(totp_token)
#             and validator.message_id_valid(message_id)):
#         return ERROR_VALIDATION
#
#     # Check token life.
#     if not validator.alive_token(user_name, totp_token):
#         return ERROR_INVALID_2FA
#     message = dao_message.get_message(message_id)
#     return str(message)


if __name__ == '__main__':
    app.run()
