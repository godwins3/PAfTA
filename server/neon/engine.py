from mt5 import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from flask import jsonify
from db.mongo_conn import create as create_mongo_conn

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
    
def fetch_performance_data(current_user):
    try:
        # Fetch performance data from the database
        client = create_mongo_conn()
        db = client[current_user['db_name']]
        trades_collection = db['trades']

        # Calculate overall performance metrics
        total_trades = trades_collection.count_documents({})
        winning_trades = trades_collection.count_documents({'profit': {'$gt': 0}})
        losing_trades = trades_collection.count_documents({'profit': {'$lt': 0}})

        if total_trades > 0:
            win_rate = (winning_trades / total_trades) * 100
        else:
            win_rate = 0

        # Calculate total profit/loss
        pipeline = [
            {'$group': {'_id': None, 'total_profit': {'$sum': '$profit'}}}
        ]
        result = list(trades_collection.aggregate(pipeline))
        total_profit = result[0]['total_profit'] if result else 0

        # Get recent trades
        recent_trades = list(trades_collection.find({}, {'_id': 0}).sort('close_time', -1).limit(10))

        performance_data = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'total_profit': round(total_profit, 2),
            'recent_trades': recent_trades
        }

        return jsonify({"data": performance_data, "message": "Performance data fetched successfully", "statusCode": 200})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to fetch performance data", "statusCode": 500}), 500
    finally:
        if 'client' in locals():
            client.close()

