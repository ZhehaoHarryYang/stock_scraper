from init_path import *  # Import the initialization script

from models.mongo_connection import get_collection
from SingleStock_History import update_historical_prices

# Connect to database
collection_Stocks = get_collection('StockList')
collection_history = get_collection('HistoryPrice')

# List to accumulate new data for bulk insert
bulk_insert_data = []

# Retrieve all stock symbols from the StockList collection
stock_symbols = collection_Stocks.distinct('symbol')

for symbol in stock_symbols:
    # Get new historical prices
    new_records = update_historical_prices(symbol)
    
    if new_records:
        bulk_insert_data.append({
            'symbol': symbol,
            'hist_price': new_records
        })
        print(f"Prepared {len(new_records)} new historical records for {symbol}")
    else: 
        print(f"no new historical records for {symbol}")

# Perform bulk insert/update
if bulk_insert_data:
    # Create bulk operations
    bulk_operations = []
    for data in bulk_insert_data:
        bulk_operations.append({
            'update_one': {
                'filter': {'symbol': data['symbol']},
                'update': {'$addToSet': {'hist_price': {'$each': data['hist_price']}}},
                'upsert': True  # Insert the document if it doesn't exist
            }
        })

    # Execute the bulk operations
    result = collection_history.bulk_write(bulk_operations)
    print(f"Bulk update result: {result.bulk_api_result}")
