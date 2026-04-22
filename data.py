import ccxt
import pandas as pd

exchange = ccxt.binance()

import requests

def get_symbols(limit=200):
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        data = requests.get(url).json()

        symbols = [
            s['symbol'] for s in data['symbols']
            if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING'
        ]

        symbols = [s.replace("USDT", "/USDT") for s in symbols]

        return symbols[:limit]

    except Exception as e:
        print("Error fetching symbols:", e)
        return []

def get_ohlcv(symbol, timeframe='1h', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print("Error:", e)
        return None