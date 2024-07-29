import requests
from lxml import etree
from models.mongo_connection import get_database, get_collection

def topMover():

    # 发送请求
    url = 'https://stockanalysis.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    # 解析响应
    e = etree.HTML(resp.text)

    info = e.xpath('//div[@class="grow"]/table/tbody/tr')
    # a = e.xpath('//div[@class="grow"]/div/a/h2/text()')

    topGainers = [{} for _ in range(10)]
    topLosers = [{} for _ in range(10)]

    for i in range(len(info)):
        tds = info[i].xpath('./td')
        ele = [td.xpath('string(.)').strip() for td in tds]
        if i >= 10:
            topLosers[i - 10]['symbol'] = ele[0]
            topLosers[i - 10]['name'] = ele[1]
            topLosers[i - 10]['price'] = ele[2]
            topLosers[i - 10]['change'] = ele[3]
        else:
            topGainers[i]['symbol'] = ele[0]
            topGainers[i]['name'] = ele[1]
            topGainers[i]['price'] = ele[2]
            topGainers[i]['change'] = ele[3]

    # print(a)
    # print(topGainers)
    # print(topLosers)

    # 获取数据库和集合
    db = get_database()
    collection_gainers = get_collection(db, 'top_gainers')
    collection_losers = get_collection(db, 'top_losers')

    # 清空集合
    collection_gainers.delete_many({})
    collection_losers.delete_many({})

    # 插入数据到 MongoDB
    if topGainers:
        collection_gainers.insert_many(topGainers)
    if topLosers:
        collection_losers.insert_many(topLosers)

    print("top movers inserted into MongoDB successfully.")

topMover()