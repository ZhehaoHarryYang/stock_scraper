from models.mongo_connection import get_collection, get_database
from SingleStock_History import get_historical_prices, update_historical_prices

# Connect to database
db = get_database()
collection_Stocks = get_collection(db, 'StockList')
collection_history = get_collection(db, 'HistoryPrice')

# Retrieve all stock symbols from the StockList collection
stock_symbols = collection_Stocks.distinct('symbol')

for symbol in stock_symbols:
    # Update historical prices or insert new data
    if collection_history.count_documents({'symbol': symbol}) > 0:
        update_historical_prices(symbol)
        print(f"Updated historical prices for {symbol}")
    else:
        stock_hist = {
            'symbol': symbol,
            'hist_price': get_historical_prices(symbol)
        }
        collection_history.insert_one(stock_hist)
        print(f"Inserted historical prices for {symbol}")
