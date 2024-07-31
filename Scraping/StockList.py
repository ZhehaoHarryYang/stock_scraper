from init_path import *  # Import the initialization script

import time
import requests
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_driver import get_chrome_driver  # Import the driver function
from models.mongo_connection import get_collection, get_database
from SingleStock_News_Detail import update_stock_info
from utils.marketCapSort import convert_market_cap_to_numeric
from pymongo import DESCENDING

# Get the Selenium driver
# driver = get_chrome_driver()

# # Open the webpage
# url = 'https://finance.yahoo.com/screener/equity/new/'
# driver.get(url)

# # Wait for the page to load completely
# time.sleep(10)  # Adjust the sleep time based on your internet speed and page load time

# # Click on tabs or buttons as necessary
# # try:
# # Example: Click on button to remove filter
# button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//button[@title='Remove Market Cap (Intraday)']"))
# )
# button.click()


# # Wait for the content to load after clicking
# time.sleep(10)  # Adjust based on the content load time



# # Example: Clicking another button
# findButton = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//button[@data-test='find-stock']"))
# )
# findButton.click()

# time.sleep(10)

# # except Exception as e:
# #     print(f"An error occurred: {e}")

# # Get the page url after find clicked
# current_url = driver.current_url
# # Get the page source after interaction
# # page_source = driver.page_source

# # Close the browser
# driver.quit()

current_url = 'https://finance.yahoo.com/screener/unsaved/048d95bc-745e-4087-9aa4-2ead70dc0830'
# Parse the page source with lxml
# e = etree.HTML(page_source)

# 获取数据库和集合
db = get_database()
collection_Stocks = get_collection(db, 'StockList')

def sort_stocks_by_market_cap():
    db = get_database()
    collection_Stocks = get_collection(db, 'StockList')
    
    # Perform a sort operation
    sorted_stocks = collection_Stocks.find().sort('MarketCapValue', DESCENDING)
    
    # Optionally, print or return sorted stocks
    for stock in sorted_stocks:
        print(stock)

for i in range(10):
    # 发送请求 
    url = current_url + f'?count=25&offset={i * 25}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'unicode'

    # 解析响应
    e = etree.HTML(resp.text)

    info = e.xpath('//table[@class="W(100%)"]/tbody/tr')

    Stocks = []

    for i in range(len(info)):
        tds = info[i].xpath('./td')
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

        # 清空集合
        if collection_Stocks.find_one({'symbol': stock_data['symbol']}):
        # If it exists, delete the document
            collection_Stocks.delete_one({'symbol': stock_data['symbol']})
            print(f"general info with {stock_data['symbol']} updated.")
        else: 
            print(f"{stock_data['symbol']} general info inserted into MongoDB successfully.")
        collection_Stocks.insert_one(stock_data)
        # get stock detail info
        print()
        update_stock_info(stock_data['symbol'])

    i += 1

sort_stocks_by_market_cap()

# driver.quit()