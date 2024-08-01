# stock_details.py
from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection
from SingleStock_Info import get_stock_info

collection_detail = get_collection('stock_details')

def fetch_stock_details(symbol):
    """Fetch stock details for a given symbol."""
    detailInfo = get_stock_info(symbol)
    if not detailInfo.get('name'):  # Check if the detailInfo is empty or None
        return None
    return detailInfo

def update_stock_details(symbol):
    detailInfo = fetch_stock_details(symbol)
    print(detailInfo)
    """Update or insert stock details into the database."""
    if collection_detail.find_one({'symbol': symbol}):
        collection_detail.update_one(
            {'symbol': symbol},  # Query to find the document
            {'$set': detailInfo},  # Update the document with detailInfo
        )
        print(f"Details with symbol {symbol} updated.")
    else:
        collection_detail.insert_one(detailInfo)
        print(f"Details with symbol {symbol} inserted.")


# update_stock_details('CSCO')