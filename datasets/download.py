import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

# Initialize MetaTrader 5 connection
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5, error code:", mt5.last_error())
    quit()

# Define symbol and timeframe
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M1  # M1 timeframe
start_date = datetime.now() - timedelta(days=7)  # Fetch data from the last 7 days
end_date = datetime.now()

# Request historical data
print(f"Fetching {symbol} M1 data from {start_date} to {end_date}...")
rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

# Check if data was retrieved
if rates is None:
    print(f"Failed to retrieve data for {symbol}, error code:", mt5.last_error())
    mt5.shutdown()
    quit()

# Convert data to pandas DataFrame
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert time to datetime
df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]  # Select desired columns

# Save to CSV
csv_file = f"{symbol}_M1_data.csv"
df.to_csv(csv_file, index=False)
print(f"Data saved to {csv_file}")

# Shutdown MetaTrader 5 connection
mt5.shutdown()
