import onetimepass as otp
import app_dao.dao_message as dao_message
import app_dao.dao_user as dao_user
from flask import Flask, url_for

app = Flask(__name__)


# Get ID of entries.
@app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['GET'])
def get_all_messages(user_name, totp_token):
    # Get the secret of the user from db.
    # Check if the token is valid.
    totp_secret = dao_user.get_user_secret(user_name)
    token_valid = otp.valid_totp(totp_token, totp_secret)
    if not token_valid:
        # TODO Redirect to error code.
        return "Invalid 2FA."

    # Fetch the ID's.
    message_ids = dao_message.get_message_ids_by_receiver(user_name)

    # Convert the Cursor returned object to a list.
    id_list = []
    for message_id in message_ids:
        id_list.append(message_id)

    # Return the list.
    return str(id_list)


# Get entry.
@app.route('/user/<user_name>/message/<message_id>', methods=['GET'])
def get_message(user_name, message_id):
    message = dao_message.get_message(message_id)
    return str(message)


# Add entry.
@app.route('/message/', methods=['POST'])
def post_message():
    return 'post_message'


# Delete entry.
@app.route('/user/<user_name>/message/<message_id>', methods=['DELETE'])
def delete_message(user_name, message_id):
    return 'delete_message' + user_name + message_id


# Delete all entries.
@app.route('/user/<user_name>/message/', methods=['DELETE'])
def delete_all_messages(user_name):
    return 'delete_all_messages' + user_name


if __name__ == '__main__':
    app.run()
