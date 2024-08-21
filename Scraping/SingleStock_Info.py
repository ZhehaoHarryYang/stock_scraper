from lxml import etree
import requests

def get_stock_info(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'unicode'
    e = etree.HTML(response.text)
    
    detailInfo = {'symbol': symbol}
    name = e.xpath('//div/section/h1/text()')
    detailInfo['name'] = name[0] if name else ''

    table = e.xpath("//div/ul/li")
    for row in table:  
        cols = row.xpath('./span/text()')
        if len(cols) == 1:
            cols.append(row.xpath('./span/fin-streamer/text()')[0])
        if cols:
            if cols[0] == 'Avg. Volume': cols[0] = 'Average Volume'
            detailInfo[cols[0]] = cols[1]
            
    overview = e.xpath("//section/div/div/div/div/div/div/p/text()")
    detailInfo['Overview'] = overview[0] if overview else ''

    website = e.xpath("//section/div/div/div/div/div/div/a/@href")
    if website:
        detailInfo['Website'] = website[0]
    else:
        detailInfo['Website'] = ''  # or assign an empty string or any other default value


    about = e.xpath("//section/div/div/div/div/div/div/div")
    for item in about:
        if len(item) == 0:
            continue
        note = item.xpath('./p//text()')[0].strip()
        key = item.xpath('./h3//text()')[0].strip()
        detailInfo[key] = note

    if not isinstance(detailInfo, dict):
        return {}
    return {k: v for k, v in detailInfo.items() if v is not None and v != ''}

def get_stock_news(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'unicode'
    e = etree.HTML(response.text)

    news = e.xpath("//div[@data-testid='news-stream']/div/div/ul/li/section")
    news_list = []
    for item in news:
        image = item.xpath('./a/div/img/@src')
        image = image[0] if image else ''
        title = item.xpath('./div/a/h3/text()')[0]
        link = item.xpath('./div/a/@href')
        link = link[0] if link else ''
        source = ('-').join(item.xpath('./div/div/div/text()'))
        news_list.append({
            'image': image,
            'title': title,
            'link': link,
            'source': source
        })

    return news_list


