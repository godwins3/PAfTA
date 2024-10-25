import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import joblib
import logging
import os
from threading import Thread, Event

# Configure logging
logging.basicConfig(filename='trading_new_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

class TradingEngine:
    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, model_path="exodus\models\exodus.joblib", risk_percentage=1):
        self.symbol = symbol
        self.timeframe = timeframe
        self.model_path = model_path
        self.running = False
        self.thread = None
        self.stop_event = Event()

        # Prepare and preprocess data
        self.n_features = 60  # Adjust based on your model and data
        
        # Risk management parameters
        self.daily_loss_limit = -500  # Daily loss limit
        self.trade_duration_limit = timedelta(hours=1)  # Maximum duration for open trades
        self.trailing_stop_threshold = 5  # Threshold to start trailing stop (in points)
        self.trailing_stop_distance = 3  # Distance to trail stop (in points)
        self.max_consecutive_losses = 3  # Maximum allowed consecutive losses
        self.current_consecutive_losses = 0  # Tracks current consecutive losses
        self.risk_percentage = risk_percentage  # Risk per trade as percentage of account balance
        self.max_open_trades = 5

        # Trade and account tracking
        self.daily_loss = 0
        self.open_trade_infos = []
        self.start_of_day = datetime.now().date()
        
        # Load the model
        if os.path.exists(model_path):
            self.loaded_model = joblib.load(model_path)
            logging.info("Model loaded successfully")
        else:
            raise FileNotFoundError(f"Model file '{model_path}' not found.")

        # Initialize MetaTrader 5
        if not mt5.initialize():
            logging.error("MetaTrader 5 initialization failed")
            raise ConnectionError("Failed to initialize MetaTrader 5")

    def fetch_and_preprocess_data(self):
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, 1000)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        
        rates_frame['return'] = rates_frame['close'].diff()
        return_range = rates_frame['return'].max() - rates_frame['return'].min()
        rates_frame['return'] = rates_frame['return'] / return_range
        
        rates_frame['label'] = rates_frame['return'].shift(-1)
        rates_frame['label'] = rates_frame['label'].apply(lambda x: 1 if x > 0.0 else 0)
        rates_frame.dropna(inplace=True)
        
        return rates_frame

    # Function to prepare features
    def prepare_features(self, rates_frame, n_features=60):
        train_x = np.empty((0, n_features))
        for i in range(n_features, len(rates_frame)):
            _x = rates_frame['return'].iloc[i-n_features:i].values.reshape(1, -1)
            train_x = np.vstack((train_x, _x))
        return train_x

    def calculate_lot_size(self):
        account_info = mt5.account_info()
        equity = account_info.equity
        risk_amount = (self.risk_percentage / 100) * equity
        return round(risk_amount / 100, 2)  # Simple calculation for lot size; refine as needed

    def log_trade_to_csv(self, trade_info):
        file_exists = os.path.isfile('trade_outcomes.csv')
        trade_info_df = pd.DataFrame([trade_info])
        trade_info_df.to_csv('trade_outcomes.csv', mode='a', header=not file_exists, index=False)

    def place_trade(self, action, slippage=5, stop_loss=15, take_profit=10):
        lot = self.calculate_lot_size()
        point = mt5.symbol_info(self.symbol).point
        price = mt5.symbol_info_tick(self.symbol).ask if action == "BUY" else mt5.symbol_info_tick(self.symbol).bid
        deviation = slippage
        
        # Calculate stop loss and take profit prices
        sl_price = price - stop_loss * point if action == "BUY" else price + stop_loss * point
        tp_price = price + take_profit * point if action == "BUY" else price - take_profit * point
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Automated trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        
        result = mt5.order_send(request)
        trade_info = {
            'time': datetime.now(),
            'symbol': self.symbol,
            'action': action,
            'lot': lot,
            'price': price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'result': 'success' if result.retcode == mt5.TRADE_RETCODE_DONE else 'failure',
            'retcode': result.retcode,
            'profit': None,
            'volume': None
        }
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            logging.info(f"Trade successful: {action} {lot} lot of {self.symbol} at {price}, SL={sl_price}, TP={tp_price}")
        else:
            logging.error(f"Trade failed, retcode={result.retcode}")
        
        return result, trade_info

    def trade_loop(self):
        while not self.stop_event.is_set():
            # Daily loss limit check
            if datetime.now().date() != self.start_of_day:
                self.start_of_day = datetime.now().date()
                self.daily_loss = 0

            if self.daily_loss <= self.daily_loss_limit:
                logging.warning("Daily loss limit reached. Halting trading for today.")
                break
            
            # Fetch and prepare data
            rates_frame = self.fetch_and_preprocess_data()
            if len(rates_frame) < 60:
                time.sleep(30)
                continue

            predictions = self.loaded_model.predict(self.prepare_features(rates_frame, n_features=60))
            latest_prediction = predictions[-1]

            # Trade based on prediction
            if latest_prediction == 0:
                result, trade_info = self.place_trade("BUY")
            else:
                result, trade_info = self.place_trade("SELL")

            # Track trade results and update loss count
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                self.current_consecutive_losses += 1
                if self.current_consecutive_losses >= self.max_consecutive_losses:
                    logging.warning("Max consecutive losses reached. Halting trading.")
                    break
            else:
                self.current_consecutive_losses = 0  # Reset on successful trade

            # Trailing stop logic can be implemented here...

            time.sleep(30)

        mt5.shutdown()
        logging.info("Trading engine stopped.")

    def start(self):
        if self.running:
            logging.warning("Trading engine is already running")
            return "Trading engine is already running"
        
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self.trade_loop)
        self.thread.start()
        return "Trading engine started"

    def stop(self):
        if not self.running:
            logging.warning("Trading engine is not running")
            return "Trading engine is not running"
        
        self.stop_event.set()
        self.thread.join()
        self.running = False
        return "Trading engine stopped"

# Example usage
# trading_engine = TradingEngine()

# Start trading engine
# print(trading_engine.start())

# Stop trading engine
# print(trading_engine.stop())
