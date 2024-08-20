from init_path import *  # Import the initialization script

import requests
from lxml import etree
from models.mongo_connection import get_collection

def topGainer():

    # 发送请求
    url = 'https://finance.yahoo.com/markets/stocks/gainers/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    # 解析响应
    e = etree.HTML(resp.text)

    info = e.xpath('//tr')

    topGainers = [{} for _ in range(len(info) -1)]

    for i in range(1,len(info)):
        tds = info[i].xpath('./td')
        text_content = []
        for j in range(len(tds)):
            # Extract text from all descendant nodes within each <td>
            tmp = tds[j].xpath('.//text()')
            txt = []
            for t in tmp:
                if t.strip():
                    txt.append(t)
            text_content.append(txt)

        topGainers[i-1]['symbol'] = text_content[0][0]
        topGainers[i-1]['name'] = text_content[0][1]
        topGainers[i-1]['price'] = text_content[1][0]
        topGainers[i-1]['change'] = text_content[2][0]
        topGainers[i-1]['changePer'] = text_content[3][0]
        topGainers[i-1]['volume'] = text_content[4][0]
        topGainers[i-1]['avgVol'] = text_content[5][0]
        topGainers[i-1]['marketCap'] = text_content[6][0]
        topGainers[i-1]['PER'] = text_content[7][0]
        topGainers[i-1]['52WChangePer'] = text_content[8][0]

            

    # print(a)
    # print(topGainers)
    # print(len(topGainers))
    # print(topLosers)

    # 获取数据库和集合
    collection_gainers = get_collection('top_gainers')

    # 清空集合
    collection_gainers.delete_many({})

    # 插入数据到 MongoDB
    if topGainers:
        collection_gainers.insert_many(topGainers)
        print("top gainer inserted into MongoDB successfully.")

def topLoser():

    # 发送请求
    url = 'https://finance.yahoo.com/markets/stocks/losers/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    # 解析响应
    e = etree.HTML(resp.text)

    info = e.xpath('//tr')
    topLosers = [{} for _ in range(len(info) -1)]

    for i in range(1,len(info)):
        tds = info[i].xpath('./td')
        text_content = []
        for j in range(len(tds)):
            # Extract text from all descendant nodes within each <td>
            tmp = tds[j].xpath('.//text()')
            txt = []
            for t in tmp:
                if t.strip():
                    txt.append(t)
            text_content.append(txt)

        topLosers[i-1]['symbol'] = text_content[0][0]
        topLosers[i-1]['name'] = text_content[0][1]
        topLosers[i-1]['price'] = text_content[1][0]
        topLosers[i-1]['change'] = text_content[2][0]
        topLosers[i-1]['changePer'] = text_content[3][0]
        topLosers[i-1]['volume'] = text_content[4][0]
        topLosers[i-1]['avgVol'] = text_content[5][0]
        topLosers[i-1]['marketCap'] = text_content[6][0]
        topLosers[i-1]['PER'] = text_content[7][0]
        topLosers[i-1]['52WChangePer'] = text_content[8][0]

        
    # print(topLosers)

    # 获取数据库和集合
    collection_losers = get_collection('top_losers')

    # 清空集合
    collection_losers.delete_many({})

    # 插入数据到 MongoDB
    if topLosers:
        collection_losers.insert_many(topLosers)
        print("top losers inserted into MongoDB successfully.")


topGainer()
topLoser()