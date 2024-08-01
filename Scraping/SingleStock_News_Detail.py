from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection, get_database
from SingleStock_Info import get_stock_info, get_stock_news
from tenacity import retry, wait_exponential, stop_after_attempt


# Retry logic with exponential backoff
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def fetch_stock_info(symbol):
    detailInfo = get_stock_info(symbol)
    if not detailInfo['name']:  # Check if the detailInfo is empty or None
        raise ValueError(f"Received empty data for symbol {symbol}")
    detailInfo['newsList'] = get_stock_news(symbol)
    return detailInfo

def update_stock_info(symbol):
    db = get_database()
    collection_detail = get_collection(db, 'stock_details')
    
    try:
        detailInfo = fetch_stock_info(symbol)
        
        if collection_detail.find_one({'symbol': symbol}):
            collection_detail.delete_one({'symbol': symbol})
            collection_detail.insert_one(detailInfo)
            print(f"Details with symbol {symbol} updated.")
        else:
            collection_detail.insert_one(detailInfo)
            print(f"Details with symbol {symbol} inserted.")
    
    except Exception as e:
        print(f"An error occurred while updating stock info for {symbol}: {e}")

# Test the function
update_stock_info('AAPL')
