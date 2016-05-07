import onetimepass as otp
import app_dao.dao_message as dao_message
import app_dao.dao_user as dao_user
from flask import Flask, url_for

app = Flask(__name__)

RESPONSE_INVALID_2FA = "Invalid 2FA."


# TODO Make shell script that would help on constructing URL for REST queries
# Like:
# $ set 2fa = 523777
# $ set method = DELETE
# $ set user = test
# $ do_curl


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
    message_ids = dao_message.get_message_ids_by_receiver(user_name)

    # Convert the Cursor returned object to a list.
    id_list = []
    for message_id in message_ids:
        id_list.append(message_id)

    # Return the list.
    return str(id_list)


# Get entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['GET'])
def get_message(user_name, totp_token, message_id):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA
    message = dao_message.get_message(message_id)
    return str(message)


# Add entry.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['POST'])
def post_message(user_name, totp_token):
    if not token_valid(user_name, totp_token):
        # TODO Redirect to error code.
        return RESPONSE_INVALID_2FA
    return 'post_message'


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


if __name__ == '__main__':
    app.run()
