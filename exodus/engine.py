import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from joblib import load
import time
from db.mongo_conn import create as create_mongo_conn

print(f"INFO: [{str(datetime.now())}] Project Neon Initiated successfully")

# Initialize MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Load the model from the file
loaded_model = load('exodus.joblib')

# Define the symbol and timeframe
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1  # Hourly data

# Print account info at start of trade
print("---------- acc info ---------")
account_info_dict = mt5.account_info()._asdict()
for key, value in account_info_dict.items():
    print(f"{key}: {value}")
print("---------- end --------------")

# Define the function to place an order
def place_order(symbol, order_type, volume, price, stop_loss, take_profit):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return result

# Define the function to close an order
def close_order(ticket, symbol, volume, price):
    position = mt5.positions_get(ticket=ticket)
    if not position:
        print(f"Position with ticket {ticket} not found")
        return None

    order_type = mt5.ORDER_TYPE_SELL if position[0].type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "position": ticket
    }

    # Send the order
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Close order failed, retcode={result.retcode}")
        result_dict = result._asdict()
        for field in result_dict.keys():
            print(f"   {field}={result_dict[field]}")
    else:
        print(f"Order closed successfully, order ID: {result.order}")

    return result

# Initialize MongoDB connection
client = create_mongo_conn()
db = client['trades']
collection = db[symbol]

# Start the trading loop
start_time = datetime.now()
end_time = start_time + timedelta(minutes=20)
trade_index = 0

while datetime.now() < end_time:
    # Fetch data
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1000)
    rates_frame = pd.DataFrame(rates)

    # Convert time in seconds to datetime
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    
    # Prepare data for model prediction
    X = rates_frame[['open', 'high', 'low', 'close', 'tick_volume']]
    df = X.copy()

    # Duplicate the column
    df['Adj Close'] = df['close']

    # Calculate return and normalize it
    df['return'] = df['Adj Close'] - df['Adj Close'].shift(1)
    return_range = df['return'].max() - df['return'].min()
    df['return'] = df['return'] / return_range

    # Create label column for model training
    df['label'] = df['return'].shift(-1)
    df['label'] = df['label'].apply(lambda x: 1 if x > 0.0 else 0)

    n_features = 60  # Number of features

    # Prepare the feature set for prediction
    train_x = np.array([]).reshape([-1, n_features])

    for index, row in df.iterrows():
        i = df.index.get_loc(index)
        if i < n_features:
            continue
        _x = np.array(df[i-n_features+1:i+1]['return']).T.reshape([1, -1])
        train_x = np.vstack((train_x, _x))

    # Make predictions
    if train_x.size > 0:
        predictions = loaded_model.predict(train_x)
        last_prediction = predictions[-1]

        order_type = mt5.ORDER_TYPE_BUY if last_prediction == 1 else mt5.ORDER_TYPE_SELL
        volume = 2.0
        trade_index = trade_index + 1
        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
        stop_loss = price - 0.00005 if order_type == mt5.ORDER_TYPE_BUY else price + 0.00005
        take_profit = price + 0.0002 if order_type == mt5.ORDER_TYPE_BUY else price - 0.0002

        trade_open_time = datetime.now()
        print(f"INFO: [{str(trade_open_time)}] Trade {trade_index} initiated")
        result = place_order(symbol, order_type, volume, price, stop_loss, take_profit)
        # print(result)

        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            ticket = result.order
            time.sleep(30)  # Sleep to simulate some time passing, replace with your actual logic
            close_price = mt5.symbol_info_tick(symbol).bid if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
            close_result = close_order(ticket, symbol, volume, close_price)
            trade_close_time = datetime.now()
            trade_duration = trade_close_time - trade_open_time
            print(f"INFO: [{str(trade_close_time)}] Trade {trade_index} closed gracefully")

            # Calculate profit or loss
            profit_loss = (close_price - price) * volume if order_type == mt5.ORDER_TYPE_BUY else (price - close_price) * volume
            outcome = "Profit" if profit_loss > 0 else "Loss"

            # Log the trade outcome
            trade_log = {
                'Order_Type': 'Buy' if order_type == mt5.ORDER_TYPE_BUY else 'Sell',
                'Volume': volume,
                'Open_Price': price,
                'Close_Price': close_price,
                'Stop_Loss': stop_loss,
                'Take_Profit': take_profit,
                'Outcome': outcome,
                'Profit_Loss': profit_loss,
                'Trade_Open_Time': trade_open_time,
                'Trade_Close_Time': trade_close_time,
                'Duration': str(trade_duration)  # Convert timedelta to string for MongoDB
            }
            # Insert the trade log into MongoDB
            collection.insert_one(trade_log)

# Close MongoDB connection
client.close()

# Shutdown MetaTrader 5
print(f"INFO: [{str(datetime.now())}] Terminating mt5 server")
mt5.shutdown()
print(f"INFO: [{str(datetime.now())}] Project Neon has stopped gracefully")
