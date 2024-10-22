import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def fetch_candlestick_data(symbol, timeframe, num_candles):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return None

    timeframes = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    
    timeframe_value = timeframes.get(timeframe)

    rates = mt5.copy_rates_from(symbol, timeframe_value, datetime.now(), num_candles)
    mt5.shutdown()

    if rates is not None:
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    else:
        return None