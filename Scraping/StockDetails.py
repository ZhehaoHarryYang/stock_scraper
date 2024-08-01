# update_stock_details.py
from init_path import *  # Import the initialization script
import time
from models.mongo_connection import get_collection
from SingleStock_News_Detail import get_stock_details

# Get database and collection
collection_Stocks = get_collection('StockList')

# Fetch stock symbols from the StockList
stock_symbols = [stock['symbol'] for stock in collection_Stocks.find()]

# Get detailed information for each stock
for symbol in stock_symbols:
    get_stock_details(symbol)
    time.sleep(3)
