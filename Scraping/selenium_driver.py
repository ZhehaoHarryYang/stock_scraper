# selenium_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_chrome_driver():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'")

    # Path to your ChromeDriver executable
    chromedriver_path = '/usr/local/chromedriver/chromedriver'

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    return driver
