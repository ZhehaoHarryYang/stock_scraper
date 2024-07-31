def convert_market_cap_to_numeric(market_cap_str):
    """ Convert market cap string to numeric value """
    if 'T' in market_cap_str:
        return float(market_cap_str.replace('T', '').strip()) * 1e12
    elif 'B' in market_cap_str:
        return float(market_cap_str.replace('B', '').strip()) * 1e9
    elif 'M' in market_cap_str:
        return float(market_cap_str.replace('M', '').strip()) * 1e6
    elif 'K' in market_cap_str:
        return float(market_cap_str.replace('K', '').strip()) * 1e3
    else:
        return float(market_cap_str.replace(',', '').strip())
