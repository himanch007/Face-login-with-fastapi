from config.database import db


async def find_user(user):
    user = dict(user)
    user_data = db.User.find_one({"email":user['email']})
    if user_data:
        return user_data
    else:
        return False

async def add_user(user):
    db.User.insert_one(dict(user))