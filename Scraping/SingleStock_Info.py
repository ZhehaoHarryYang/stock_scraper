import time
# import requests
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_driver import get_chrome_driver  # Import the driver function
from models.mongo_connection import get_collection, get_database


# Get the Selenium driver
driver = get_chrome_driver()

# Open the webpage
# connect to database
db = get_database()
collection_detail = get_collection(db, 'stock_details')

def get_stock_info(symbol):
    # send to which url
    url = f"https://finance.yahoo.com/quote/{symbol}/"
    driver.get(url)
    time.sleep(15)  # Adjust the sleep time based on your internet speed and page load time

    page_source = driver.page_source

    # Parse the page source with lxml
    e = etree.HTML(page_source)

    # a dict for insert
    detailInfo = {'symbol': symbol}
    name = e.xpath('//div/section/h1/text()')
    detailInfo['name'] = name[0] if name else ''

    # 提取表格数据 Overview
    table = e.xpath("//div/ul/li")

    for row in table:  
        cols = row.xpath('./span/text()')
        if len(cols) == 1:
            cols.append(row.xpath('./span/fin-streamer/text()')[0])
        # Insert the data into the detailInfo dictionary
        if len(cols) == 2:  # Ensure there are exactly 2 spans
            detailInfo[cols[0]] = cols[1]
    
    # get the about info
    about = e.xpath("//div/div/div/p/text()")
    about = about[0] if about else ''
    
    detailInfo['Overview'] = about

    detailInfo['newsList'] = []

    # Find the elements using xpath
    news = e.xpath("//div[@id='tabpanel-news']/div/section/div/section")
    for i in range(len(news)):
        image = news[i].xpath('./a/div/img/@src')
        image = image[0] if image else ''
        title = news[i].xpath('./div/a/h3/text()')[0]
        link = news[i].xpath('./a/@href')
        link = link[0] if link else ''
        source = ('-').join(news[i].xpath('./div/div/div/text()'))
        data = {
            'image': image,
            'title': title,
            'link': link,
            'source': source
            }
        detailInfo['newsList'].append(data)
    # print(detailInfo)

    # 清空集合
    if collection_detail.find_one({'symbol': symbol}):
    # If it exists, delete the document
        collection_detail.delete_one({'symbol': symbol})
        print(f"Details with symbol {symbol} updated.")
    # 插入数据到 MongoDB
    else:
        print(f"Details with symbol {symbol} inserted.")
    collection_detail.insert_one(detailInfo)


# # get the stocks info and news
stock_symbol = ['ACGBY', 'AAPL']
for s in stock_symbol:
    stock_info = get_stock_info(s)

