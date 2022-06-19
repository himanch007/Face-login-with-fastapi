from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')

db_connection = mongo_host + ':' + mongo_port

conn = MongoClient(db_connection)