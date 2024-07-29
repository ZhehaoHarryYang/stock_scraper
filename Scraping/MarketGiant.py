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
url = 'https://finance.yahoo.com/screener/equity/new/'
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time based on your internet speed and page load time

# try:
# Example: Click on button to remove filter
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@title='Remove Market Cap (Intraday)']"))
)
button.click()


# Wait for the content to load after clicking
time.sleep(5)  # Adjust based on the content load time



# Example: Clicking another button
findButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-test='find-stock']"))
)
findButton.click()

time.sleep(5)

    
# except Exception as e:
#     print(f"An error occurred: {e}")

# Get the page source after interaction
page_source = driver.page_source

# Close the browser
driver.quit()

# Parse the page source with lxml
e = etree.HTML(page_source)

info = e.xpath('//table[@class="W(100%)"]/tbody/tr')

MarketGiant = []

# 获取数据库和集合
db = get_database()
collection_MarketGiant = get_collection(db, 'MarketGiant')

# 清空集合
collection_MarketGiant.delete_many({})

for i in range(len(info)):
# for i in range(2):
    tds = info[i].xpath('./td')
    ele = [td.xpath('string(.)').strip() for td in tds]

    stock_data = {
        'symbol': ele[0],
        'name': ele[1],
        'price': ele[2],
        'change': ele[3],
        'perChange': ele[4],
        'volume': ele[5],
        'averageVolume': ele[6],
        'MarketCap': ele[7],
        'PER': ele[8]
    }
    MarketGiant.append(stock_data)
    

# 插入数据到 MongoDB
if MarketGiant:
    collection_MarketGiant.insert_many(MarketGiant)
    print("Market Giant inserted into MongoDB successfully.")
