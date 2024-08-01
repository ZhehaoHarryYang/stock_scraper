# update_stock_details.py
from init_path import *  # Import the initialization script
from models.mongo_connection import get_collection
from Scraping.SingleStock_News import update_stock_news

# Get database and collection
collection_Stocks = get_collection('StockList')

# Fetch stock symbols from the StockList
stock_symbols = [stock['symbol'] for stock in collection_Stocks.find()]

# Get detailed information for each stock
for symbol in stock_symbols:
    update_stock_news(symbol)
