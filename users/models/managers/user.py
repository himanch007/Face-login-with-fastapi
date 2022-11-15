from config.database import conn
from bson import ObjectId
import datetime

db = conn['User']


class UserManager:
    def __init__(self):
        pass
    async def find_user(self, user):
        user = dict(user)
        if 'email' in user:
            user_data = db.find_one({"email":user['email']})
        if 'id' in user:
            user_data = db.find_one({"_id":ObjectId(user['id'])})
        if user_data:
            return user_data
        
        return False

    async def add_user(self, user):
        user = dict(user)
        user['meta']= {
            'createdOn': datetime.datetime.now()
        }
        db.insert_one(dict(user))
