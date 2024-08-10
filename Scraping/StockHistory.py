from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection
from SingleStock_History import update_historical_prices

# Connect to database
collection_Stocks = get_collection('StockList')
collection_history = get_collection('HistoryPrice')

# Retrieve all stock symbols from the StockList collection
stock_symbols = collection_Stocks.distinct('symbol')
# record the failure symbols to manual add
failed_stocks = []

for symbol in stock_symbols:
    # Get new historical prices
    new_records = update_historical_prices(symbol)
    if new_records == False:
        failed_stocks.append(symbol)
    elif new_records:
        # Prepare the data for single insert
        update_data = {
            'symbol': symbol,
            'hist_price': new_records
        }
        try:
            # Update or insert the document
            result = collection_history.update_one(
                {'symbol': symbol},
                {'$addToSet': {'hist_price': {'$each': new_records}}},
                upsert=True  # Insert the document if it doesn't exist
            )
            print(f"Updated {len(new_records)} historical records for {symbol}. Matched count: {result.matched_count}, Modified count: {result.modified_count}")
        except Exception as e:
            print(f"Error updating records for {symbol}: {e}")
    else: 
        print(f"No new historical records for {symbol}")

print(failed_stocks)