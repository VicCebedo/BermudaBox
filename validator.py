import app_dao.dao_user as dao_user
import onetimepass as otp


# Get the secret of the user from db.
# Check if the token is valid.
def alive_token(user_name, totp_token):
    totp_secret = dao_user.get_user_secret(user_name)
    token_valid = otp.valid_totp(totp_token, totp_secret)
    return token_valid


# If the length of the string <= to the len to check.
def is_len(str, len_to_check):
    if len(str) <= len_to_check:
        return True
    return False


# Check length of username.
def user_name_valid(user_name):
    if is_len(user_name, 16):
        return True
    return False


# Check length of message ID.
def message_id_valid(m_id):
    if is_len(m_id, 30):
        return True
    return False


# Check length of content.
def content_valid(content):
    if is_len(content, 300):
        return True
    return False


# Check length of 2FA.
def totp_valid(totp_token):
    if is_len(totp_token, 16):
        return True
    return False
