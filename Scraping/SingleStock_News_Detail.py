from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection, get_database
from SingleStock_Info import get_stock_info, get_stock_news

def update_stock_info(symbol):
    db = get_database()
    collection_detail = get_collection(db, 'stock_details')
    detailInfo = get_stock_info(symbol)
    detailInfo['newsList'] = get_stock_news(symbol)
    print(detailInfo)
    if collection_detail.find_one({'symbol': symbol}):
        collection_detail.delete_one({'symbol': symbol})
        collection_detail.insert_one(detailInfo)
        print(f"Details with symbol {symbol} updated.")
    else:
        collection_detail.insert_one(detailInfo)
        print(f"Details with symbol {symbol} inserted.")


update_stock_info('tm')