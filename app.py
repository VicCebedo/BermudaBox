from flask import Flask, url_for

app = Flask(__name__)


# Get ID of entries.
@app.route('/user/<user_name>/message/', methods=['GET'])
def get_all_messages():
    return 'Welcome'


# Get entry.
@app.route('/user/<user_name>/message/<message_id>', methods=['GET'])
def get_message():
    return 'Welcome'


# Add entry.
@app.route('/message/', methods=['POST'])
def post_message():
    return 'Welcome'


# Delete entry.
@app.route('/user/<user_name>/message/<message_id>', methods=['DELETE'])
def delete_message():
    return 'Welcome'


# Delete all entries.
@app.route('/user/<user_name>/message/', methods=['DELETE'])
def delete_all_messages():
    return 'Welcome'


if __name__ == '__main__':
    app.run()
