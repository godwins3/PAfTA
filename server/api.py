from flask import Flask, jsonify, render_template, request
from users.auth.signup import user_register
from users.auth.login import login
from users.auth.password_reset import reset_password, request_password_reset
from middleware.service import token_required, log_request, handle_errors
from exodus.engine import TradingEngine
from neon.trades import fetch_trade_logs, fetch_trade_logs_by_timeframe
from neon.engine import fetch_candlestick_data, fetch_current_account_info, fetch_current_position, fetch_news, fetch_performance_data

app = Flask(__name__)

trading_engine = TradingEngine()

@app.route("/", methods=["GET"])
def exodus():
    return render_template('index.html')

@app.route("/api/v1/login", methods=["POST"])
@log_request
def user_login():
    msg_received = request.get_json()
    return login(msg_received)

@app.route("/api/v1/signup", methods=["POST"])
@log_request
def signup():
    msg_received = request.get_json()
    return user_register(msg_received)

@app.route("/api/v1/protected", methods=["GET"])
@token_required
@log_request
def protected(current_user):
    return jsonify({"message": f"Hello, {current_user['name']}!", "statusCode": 200})

@app.route('/api/v1/start-trading', methods=['POST'])
# @token_required
@log_request
def api_start_trading():
    result = trading_engine.start()
    return jsonify({"message": result})

@app.route('/api/v1/stop-trading', methods=['POST'])
# @token_required
@log_request
def api_stop_trading():
    result = trading_engine.stop()
    return jsonify({"message": result})
    

@app.route("/dashboard", methods=["GET"])
# @token_required
@log_request
def dashboard():
    return render_template('dashboard/main.html')

@app.route("/login")
def login_page():
    return render_template('auth/login.html')

@app.route("/signup")
def signup_page():
    return render_template('auth/signup.html')

@app.route("/forgot-password")
def forgot_password_page():
    return render_template('auth/forgot-password.html')

@app.route("/reset-password")
def reset_password_page():
    return render_template('auth/reset-password.html')

@app.route("/api/v1/request-password-reset", methods=["POST"])
@log_request
def password_reset():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"Message": "Email is required", "statusCode": 400})
    return jsonify(request_password_reset(email))

@app.route("/api/v1/reset-password", methods=["POST"])
@log_request
def reset_password():
    data = request.get_json()
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')
    if not reset_token or not new_password:
        return jsonify({"Message": "Reset token and new password are required", "statusCode": 400})
    return jsonify(reset_password(reset_token, new_password))

@app.route("/api/v1/get-trades", methods=['GET'])
@token_required
@log_request
def get_trades():
    return fetch_trade_logs()

@app.route("/api/v1/get-trades-by-time", methods=['POST'])
@token_required
@log_request
def get_trades_by_time():
    data = request.get_json()
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    return fetch_trade_logs_by_timeframe(start_time, end_time)
    
@app.route("/api/v1/get-candlestick-data", methods=["GET"])
# @token_required
@log_request
def get_candlestick_data():
    symbol = "EURUSD"  # Change this to your desired symbol
    timeframe = "M1"   # Change this to your desired timeframe
    num_candles = 100  # Number of candlesticks to fetch

    df = fetch_candlestick_data(symbol, timeframe, num_candles)

    if df is not None:
        data = {
            'time': df['time'].tolist(),
            'open': df['open'].tolist(),
            'high': df['high'].tolist(),
            'low': df['low'].tolist(),
            'close': df['close'].tolist(),
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500
    
@app.route("/api/v1/get-current-position", methods=["GET"])
@token_required
@log_request
def get_current_position():
    return fetch_current_position()

@app.route("/api/v1/get-current-account-info", methods=["GET"])
@token_required
@log_request
def get_current_account_info():
    return fetch_current_account_info()

@app.route("/api/v1/news", methods=['GET'])
@token_required
@log_request
def get_news():
    return fetch_news()

@app.route("/dashboard/settings")
@token_required
@log_request
def settings_page():
    return render_template('dashboard/settings.html')

@app.route("/api/v1/update-settings", methods=["POST"])
@token_required
@log_request
def update_settings():
    data = request.get_json()
    return jsonify({"message": "Settings updated successfully", "statusCode": 200})

@app.route("/api/v1/performance-data")
@token_required
@log_request
def get_performance_data(current_user):
    return fetch_performance_data(current_user)
        
handle_errors(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
