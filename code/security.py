import hmac
from models.auth import Auth

def authenticate(username, password):
    user = Auth.find_by_username(username)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identify(payload):
    user_id = payload['identity']
    return Auth.find_by_id(user_id)