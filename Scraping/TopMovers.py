from init_path import *  # Import the initialization script

import requests
from lxml import etree
from models.mongo_connection import get_collection

def fetch_data(url):
    """Fetches and returns the parsed HTML data from the given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'unicode'
        return etree.HTML(response.text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_table_rows(html_element):
    """Parses table rows and returns a list of dictionaries with stock data."""
    rows = html_element.xpath('//tr')
    stock_data = []

    for row in rows[1:]:  # Skip the header row
        cells = row.xpath('./td')
        text_content = [cell.xpath('.//text()') for cell in cells]
        text_content = [[t.strip() for t in cell if t.strip()] for cell in text_content]
        
        if len(text_content) < 9:
            continue  # Skip rows that don't have the expected number of columns

        stock = {
            'symbol': text_content[0][0],
            'name': text_content[0][1],
            'price': text_content[1][0],
            'change': text_content[2][0],
            'changePer': text_content[3][0],
            'volume': text_content[4][0],
            'avgVol': text_content[5][0],
            'marketCap': text_content[6][0],
            'PER': text_content[7][0],
            'YearChangePer': text_content[8][0]
        }
        stock_data.append(stock)

    return stock_data

def update_collection(collection_name, data):
    """Updates the MongoDB collection with the provided data."""
    collection = get_collection(collection_name)
    collection.delete_many({})
    if data:
        collection.insert_many(data)
        print(f"{collection_name} inserted into MongoDB successfully.")

def top_gainers():
    """Fetches and processes top gainers data."""
    url = 'https://finance.yahoo.com/markets/stocks/gainers/'
    html_element = fetch_data(url)
    if html_element is not None:
        top_gainers_data = parse_table_rows(html_element)
        update_collection('top_gainers', top_gainers_data)

def top_losers():
    """Fetches and processes top losers data."""
    url = 'https://finance.yahoo.com/markets/stocks/losers/'
    html_element = fetch_data(url)
    if html_element is not None:
        top_losers_data = parse_table_rows(html_element)
        update_collection('top_losers', top_losers_data)

def trending_now():
    url = 'https://finance.yahoo.com/markets/stocks/trending/'
    html_element = fetch_data(url)
    if html_element is not None:
        trending_now_data = parse_table_rows(html_element)
        update_collection('trending_now', trending_now_data)

def most_active():
    url = 'https://finance.yahoo.com/markets/stocks/most-active/'
    html_element = fetch_data(url)
    if html_element is not None:
        most_active_data = parse_table_rows(html_element)
        update_collection('most_active', most_active_data)

def year_top_gainers():
    url = 'https://finance.yahoo.com/markets/stocks/52-week-gainers/'
    html_element = fetch_data(url)
    if html_element is not None:
        year_top_gainers_data = parse_table_rows(html_element)
        update_collection('year_top_gainers', year_top_gainers_data)

def year_top_losers():
    url = 'https://finance.yahoo.com/markets/stocks/52-week-losers/'
    html_element = fetch_data(url)
    if html_element is not None:
        year_top_losers_data = parse_table_rows(html_element)
        update_collection('year_top_losers', year_top_losers_data)


if __name__ == "__main__":
    top_gainers()
    top_losers()
    trending_now()
    most_active()
    year_top_gainers()
    year_top_losers()
