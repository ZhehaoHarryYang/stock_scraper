from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the MongoDB URI from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

def get_database():
    # 提供MongoDB的连接字符串
    client = MongoClient(MONGODB_URI)
    
    # 选择数据库
    db = client['Stock_Web']
    return db

def get_collection(db, collection_name):
    # 选择集合
    collection = db[collection_name]
    return collection
