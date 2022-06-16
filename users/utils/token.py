import jwt, datetime
from config.settings import SECRET_KEY


def get_access_token(user):
    payload = {
            'id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }
    return jwt.encode(payload, SECRET_KEY)

def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])