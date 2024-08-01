from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection, get_database
from SingleStock_Info import get_stock_info, get_stock_news

def fetch_stock_info(symbol):
    detailInfo = get_stock_info(symbol)
    detailInfo['newsList'] = get_stock_news(symbol)
    if not detailInfo.get('name'):  # Check if the detailInfo is empty or None
        return None
    return detailInfo

def get_stock_details(symbol):
    db = get_database()
    collection_detail = get_collection(db, 'stock_details')

    # First attempt to fetch stock info
    detailInfo = fetch_stock_info(symbol)
    
    if detailInfo is None:  # If data is empty, retry once
        print(f"Received empty data for symbol {symbol}. Retrying...")
        detailInfo = fetch_stock_info(symbol)
        if detailInfo is None: 
            return

    if collection_detail.find_one({'symbol': symbol}):
        collection_detail.update_one(
            {'symbol': symbol},  # Query to find the document
            {'$set': detailInfo},  # Update the document with detailInfo
        )
        print(f"Details with symbol {symbol} updated.")
    else:
        collection_detail.insert_one(detailInfo)
        print(f"Details with symbol {symbol} inserted.")

# Test the function
# get_stock_details('GE')
