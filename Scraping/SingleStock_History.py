import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

from models.mongo_connection import get_database, get_collection


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    return date_obj.strftime("%Y-%m-%d")

def get_historical_prices(symbol):
    # send to which url
    url = f'https://finance.yahoo.com/quote/{symbol}/history/'

    # camouflage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # send request
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    soup = BeautifulSoup(resp.text, 'html.parser')

    # 提取表格数据
    table = soup.find('table', {'class': "table yf-ewueuo"})
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  # 跳过表头
        cols = row.find_all('td')
        if len(cols) == 7:
            cols = [col.text.strip() for col in cols]
            cols[0] = convert_date(cols[0])
            data.append(cols)
    
    # 将数据转换为 DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume'])
    df['symbol'] = symbol  # 添加股票符号列
    records = df.to_dict(orient='records')
    return records

def update_historical_prices(symbol):
    # 获取新的历史价格数据
    new_records = get_historical_prices(symbol)
    
    # 获取数据库和集合
    db = get_database()
    collection = get_collection(db, 'HistoryPrice')
    
    # 获取现有数据中最新的日期
    pipeline = [
        {"$match": {"symbol": symbol}},  # 匹配符号为 AAPL 的文档
        {"$unwind": "$hist_price"},  # 将 hist_price 数组展开成单独的文档
        {"$sort": {"hist_price.Date": -1}},  # 按 hist_price 中的日期降序排序
        {"$group": {
            "_id": "$_id", 
            "symbol": {"$first": "$symbol"}, 
            "hist_price": {"$push": "$hist_price"}
        }},  # 将文档重新分组并聚合 hist_price 数组
        {"$project": {"_id": 0, "symbol": 1, "hist_price": {"$slice": ["$hist_price", 10]}}}  # 投影并限制 hist_price 数组中的元素数量为 10
    ]
    
    latest_record = collection.aggregate(pipeline)
    latest_date = ''
    for result in latest_record:
        latest_date = result['hist_price'][0]['Date']
    print(latest_date)
    filtered_records = []
    for record in new_records:
        if record['Date'] > latest_date:
            filtered_records.append(record)
        else:
            break

    # Update the existing document for 'AAPL' with filtered records
    result = collection.update_one(
        {'symbol': symbol},
        {'$addToSet': {'hist_price': {'$each': filtered_records}}},
        upsert=True  # Insert the document if it doesn't exist
    )
    if result.modified_count > 0 or result.upserted_id:
        print(f"Inserted {len(filtered_records)} new records into the {symbol} document.")
    else:
        print(f"No new records to insert or update for {symbol}.")

