import requests
import onetimepass as otp
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

SUCCESS_MESSAGE_SENT = "Message sent."
SUCCESS_USER_CREATED = "User created. Secret Key: "
SUCCESS_MESSAGE_DELETE = "Deleted message."
SUCCESS_MESSAGE_DELETE_ALL = "Deleted all messages: "


# TODO Make AngularJS-based web interface, set user_name in cookie.

# Get the secret of the user from db.
# Check if the token is valid.
def token_valid(user_name, totp_token):
    totp_secret = dao_user.get_user_secret(user_name)
    token_valid = otp.valid_totp(totp_token, totp_secret)
    return token_valid


# Get ID of entries.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['GET'])
def get_all_messages(user_name, totp_token):
    # Check if user exists.
    if not dao_user.user_exists(user_name):
        return ERROR_N0_USER + user_name

    # Check 2FA.
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return ERROR_INVALID_2FA

    # Fetch the ID's.
    message_ids = dao_message.get_all_messages(user_name)
    return json_util.dumps(message_ids)


# Verify recaptcha.
@app.route('/recaptcha/siteverify', methods=['POST'])
def recaptcha_verify():
    requestData = request.data

    # TODO Find a better way of extracting data from request.
    secret = request.json[0].get('secret')
    response = request.json[1].get('response')

    # Verify in google.
    googleResponse = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                   data={'secret': secret, 'response': response})
    success = json_util.loads(googleResponse.text)['success']
    return str(success).lower()


# Get entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['GET'])
def get_message(user_name, totp_token, message_id):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return ERROR_INVALID_2FA
    message = dao_message.get_message(message_id)
    return str(message)


# Delete entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['DELETE'])
def delete_message(user_name, totp_token, message_id):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return ERROR_INVALID_2FA
    dao_message.delete_message(message_id)
    return SUCCESS_MESSAGE_DELETE


# Delete all entries.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['DELETE'])
def delete_all_messages(user_name, totp_token):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return ERROR_INVALID_2FA
    dao_message.delete_all_messages(user_name)
    return SUCCESS_MESSAGE_DELETE_ALL + user_name


# Add user.
@app.route('/user/<user_name>/', methods=['POST'])
def post_user(user_name):
    # Check if already exists.
    if dao_user.user_exists(user_name):
        return ERROR_USER_EXISTS

    totp_secret = dao_user.create_user(user_name)
    return SUCCESS_USER_CREATED + totp_secret


# Add entry.
@app.route('/user/<receiver_user_name>/sender/<sender_user_name>/2fa/<totp_token>/message/', methods=['POST'])
def post_message(receiver_user_name, sender_user_name, totp_token):
    # Check if receiver exists.
    if not dao_user.user_exists(receiver_user_name):
        return ERROR_N0_USER + receiver_user_name

    # Check if sender exists.
    if not dao_user.user_exists(sender_user_name):
        return ERROR_N0_USER + sender_user_name

    # Check if valid 2FA.
    if not token_valid(sender_user_name, totp_token):
        # TODO Redirect to error code.
        return ERROR_INVALID_2FA

    # Do operation.
    content = json_util.Binary.decode(request.data)
    dao_message.post_message(sender_user_name, receiver_user_name, content)
    return SUCCESS_MESSAGE_SENT


# Add entry as anonymous.
@app.route('/user/<receiver_user_name>/sender/anon/message/', methods=['POST'])
def post_message_anon(receiver_user_name):
    # Check if receiver exists.
    if not dao_user.user_exists(receiver_user_name):
        return ERROR_N0_USER

    # Do operation.
    content = request.data
    dao_message.post_message("anon", receiver_user_name, content)
    return SUCCESS_MESSAGE_SENT


if __name__ == '__main__':
    app.run()
