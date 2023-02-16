from pymongo import MongoClient
import os
from dotenv import load_dotenv
from core.settings import DATABASE_NAME

load_dotenv()

mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_cluster = os.getenv('MONGO_CLUSTER')
mongo_cluster_db = os.getenv('MONGO_CLUSTER_DB')

if mongo_host and mongo_port:
    db_connection = mongo_host + ':' + mongo_port

if mongo_username and mongo_password:
    db_connection = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster}/{mongo_cluster_db}"

conn = MongoClient(db_connection)[DATABASE_NAME]
