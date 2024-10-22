import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from flask import jsonify

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
    
def fetch_current_account_info():
    # Initialize MetaTrader 5 connection
    if not mt5.initialize():
        return jsonify({'error': 'initialize() failed'}), 500

    # Fetch account information
    account_info = mt5.account_info()

    # Shutdown connection to MT5
    mt5.shutdown()

    # Check if account information is retrieved successfully
    if account_info is not None:
        balance = account_info.balance  # Get account balance
        equity = account_info.equity    # Get account equity
        free_margin = account_info.margin_free  # Get free margin

        return jsonify({
            'balance': balance,
            'equity': equity,
            'free_margin': free_margin
        })
    else:
        return jsonify({'error': 'Failed to get account information'}), 500
    
def fetch_current_position():
    # Initialize MetaTrader 5 connection
    if not mt5.initialize():
        return jsonify({'error': 'initialize() failed'}), 500

    # Get open positions
    positions = mt5.positions_get()

    # Shutdown connection to MT5
    mt5.shutdown()

    # Check if positions are retrieved successfully
    if positions is not None and len(positions) > 0:
        position_data = []
        for position in positions:
            position_data.append({
                'symbol': position.symbol,
                'type': position.type,
                'volume': position.volume,
                'price_open': position.price_open,
                'profit': position.profit
            })
        return jsonify(position_data)
    else:
        return jsonify({'error': 'No open positions found'}), 404
    
def fetch_news():
    # Initialize MetaTrader 5 connection
    if not mt5.initialize():
        return jsonify({'error': 'initialize() failed'}), 500

    # Fetch news
    news = mt5.copy_news()

    # Shutdown connection to MT5
    mt5.shutdown()

    # Check if news is retrieved successfully
    if news is not None:
        news_data = []
        for item in news:
            news_data.append({
                'title': item.title,
                'description': item.description,
                'datetime': item.datetime,
                'url': item.url
            })
        return jsonify(news_data)
    else:
        return jsonify({'error': 'No news found'}), 404
