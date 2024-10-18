import requests

def fetch_candlesticks_data():
    res = requests.get(f'https://www.mql5.com/')
    return res