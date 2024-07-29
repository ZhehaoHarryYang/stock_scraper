from pymongo import MongoClient

def get_database():
    # 提供MongoDB的连接字符串
    client = MongoClient('mongodb://localhost:27017/')
    
    # 选择数据库
    db = client['Stock_Web']
    return db

def get_collection(db, collection_name):
    # 选择集合
    collection = db[collection_name]
    return collection
