import json
import onetimepass as otp
import app_dao.dao_message as dao_message
import app_dao.dao_user as dao_user
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RESPONSE_INVALID_2FA = "Invalid 2FA."
RESPONSE_N0_USER = "User does not exist."
RESPONSE_POST_MESSAGE = "Posted message."


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
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA

    # Fetch the ID's.
    message_ids = dao_message.get_all_messages(user_name)

    # Convert the Cursor returned object to a list.
    id_list = []
    for message_id in message_ids:
        id_list.append(message_id)
    return json.dumps(str(id_list))


# Get entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['GET'])
def get_message(user_name, totp_token, message_id):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA
    message = dao_message.get_message(message_id)
    return str(message)


# Delete entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['DELETE'])
def delete_message(user_name, totp_token, message_id):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA
    dao_message.delete_message(message_id)
    return 'Deleted message: ' + user_name + ' ' + message_id


# Delete all entries.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['DELETE'])
def delete_all_messages(user_name, totp_token):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA
    dao_message.delete_all_messages(user_name)
    return 'Deleted all messages: ' + user_name


# Add user.
@app.route('/user/<user_name>/', methods=['POST'])
def post_user(user_name):
    # Check if already exists.
    if dao_user.user_exists(user_name):
        return "User already exists."

    totp_secret = dao_user.create_user(user_name)
    return "User created. TOTP Secret: " + totp_secret


# Add entry.
@app.route('/user/<receiver_user_name>/sender/<sender_user_name>/2fa/<totp_token>/message/', methods=['POST'])
def post_message(receiver_user_name, sender_user_name, totp_token):
    # Check if receiver exists.
    if not dao_user.user_exists(receiver_user_name):
        return RESPONSE_N0_USER

    # Check if valid 2FA.
    if not token_valid(sender_user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA

    # Do operation.
    content = request.data
    dao_message.post_message(sender_user_name, receiver_user_name, content)
    return RESPONSE_POST_MESSAGE


# Add entry as anonymous.
@app.route('/user/<receiver_user_name>/sender/anon/message/', methods=['POST'])
def post_message_anon(receiver_user_name):
    # Check if receiver exists.
    if not dao_user.user_exists(receiver_user_name):
        return RESPONSE_N0_USER

    # Do operation.
    content = request.data
    dao_message.post_message("anon", receiver_user_name, content)
    return RESPONSE_POST_MESSAGE


if __name__ == '__main__':
    app.run()
