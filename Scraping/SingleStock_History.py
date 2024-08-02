from init_path import *  # Import the initialization script

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

from models.mongo_connection import get_collection


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    return date_obj.strftime("%Y-%m-%d")

def get_historical_prices(symbol):
    # send to which url
    url = f'https://finance.yahoo.com/quote/{symbol}/history/'

    session = requests.Session()

    # camouflage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # send request
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None
    
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
    if new_records == None: return None
    # 获取数据库和集合
    collection = get_collection('HistoryPrice')
    
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

    filtered_records = []
    for record in new_records:
        if record['Date'] > latest_date:
            filtered_records.append(record)
        else:
            break
    # Return the filtered records instead of inserting
    return filtered_records


