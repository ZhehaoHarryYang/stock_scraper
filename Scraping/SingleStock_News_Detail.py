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

    attempts = 2
    # First attempt to fetch stock info
    detailInfo = None
    
    for attempt in range(attempts):
        detailInfo = fetch_stock_info(symbol)
        if detailInfo is not None:
            break
        print(f"Attempt {attempt + 1}: Received empty data for symbol {symbol}. Retrying...")

    if detailInfo is None:  # If still empty after all attempts
        print(f"Failed to get valid data for symbol {symbol} after {attempts} attempts.")
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
