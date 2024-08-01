# stock_news.py
from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection
from SingleStock_Info import get_stock_news

collection_news = get_collection('stock_news')

def fetch_stock_news(symbol):
    """Fetch stock news for a given symbol."""
    newsList = get_stock_news(symbol)
    if not newsList:  # Check if the newsList is empty
        return None
    return newsList

def update_stock_news(symbol):
    newsList = fetch_stock_news(symbol)
    """Update or insert stock news into the database."""
    if collection_news.find_one({'symbol': symbol}):
        collection_news.update_one(
            {'symbol': symbol},  # Query to find the document
            {'$set': {'newsList': newsList}},  # Update the document with newsList
        )
        print(f"News for symbol {symbol} updated.")
    else:
        collection_news.insert_one({'symbol': symbol, 'newsList': newsList})
        print(f"News for symbol {symbol} inserted.")

# update_stock_news('NTTYY')