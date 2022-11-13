from config.database import conn
from bson import ObjectId
import datetime
from pydantic import BaseConfig

db = conn['User']
BaseConfig.arbitrary_types_allowed = True


class UserManager:
    async def find_user(user):
        user = dict(user)
        if 'email' in user:
            user_data = db.find_one({"email":user['email']})
        if 'id' in user:
            user_data = db.find_one({"_id":ObjectId(user['id'])})
        if user_data:
            return user_data
        
        return False

    async def add_user(user):
        user = dict(user)
        user['meta']= {
            'createdOn': datetime.datetime.now()
        }
        db.insert_one(dict(user))
