from init_path import *  # Import the initialization script

import requests
from lxml import etree
from models.mongo_connection import get_collection, get_database
from utils.marketCapSort import convert_market_cap_to_numeric

# Set the URL for scraping
current_url = 'https://finance.yahoo.com/screener/unsaved/048d95bc-745e-4087-9aa4-2ead70dc0830'

# Get database and collection
db = get_database()
collection_Stocks = get_collection(db, 'StockList')
Stocks = []

for i in range(10):
    # Send request
    url = f'{current_url}?offset={i*25}&count=25'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    # Parse response
    e = etree.HTML(resp.text)
    info = e.xpath('//table[@class="W(100%)"]/tbody/tr')

    for row in info:
        tds = row.xpath('./td')
        ele = [td.xpath('string(.)').strip() for td in tds]

        stock_data = {
            'symbol': ele[0].upper(),
            'name': ele[1],
            'price': ele[2],
            'change': ele[3],
            'perChange': ele[4],
            'volume': ele[5],
            'averageVolume': ele[6],
            'MarketCap': ele[7],
            'PER': ele[8]
        }
        stock_data['MarketCapValue'] = convert_market_cap_to_numeric(stock_data['MarketCap'])

        # Update or insert stock data
        if collection_Stocks.find_one({'symbol': stock_data['symbol']}):
            collection_Stocks.delete_one({'symbol': stock_data['symbol']})
            print(f"General info with symbol {stock_data['symbol']} updated.")
        else:
            print(f"General info with symbol {stock_data['symbol']} inserted into MongoDB successfully.")

        Stocks.append(stock_data)

# Insert all the stocks
collection_Stocks.insert_many(Stocks)
print(f"{len(Stocks)} stocks inserted into MongoDB successfully.")
