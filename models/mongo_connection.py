from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the MongoDB URI from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

def get_database():
    client = MongoClient(MONGODB_URI)
    print("Connected to MongoDB Atlas successfully")
    # # List databases to verify connection
    # databases = client.list_database_names()
    # print("Databases:", databases)
    db = client['Stock_Web']

    return db

db = get_database()

def get_collection(collection_name):
    # Choose the collection
    collection = db[collection_name]
    return collection

