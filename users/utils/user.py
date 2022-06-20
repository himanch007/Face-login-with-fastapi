from config.database import conn
from config.settings import DATABASE_NAME, USER_COLLECTION
from bson import ObjectId
import datetime

db = conn[DATABASE_NAME][USER_COLLECTION]

async def find_user(user):
    user = dict(user)
    if 'email' in user:
        user_data = db.find_one({"email":user['email']})
    if 'id' in user:
        user_data = db.find_one({"_id":ObjectId(user['id'])})
    if user_data:
        return user_data
    else:
        return False

async def add_user(user):
    user = dict(user)
    user['meta']= {
        'createdOn': datetime.datetime.now()
    }
    db.insert_one(dict(user))