from flask import Flask, jsonify, render_template, request
from users.auth import login, signup, password_reset
from middleware.service import token_required, log_request, handle_errors
from exodus.engine import start_trading, stop_trading
from neon.trades import fetch_trade_logs, fetch_trade_logs_by_timeframe
from neon.engine import fetch_candlesticks_data

app = Flask(__name__)

@app.route("/", methods=["GET"])
def exodus():
    return render_template('index.html')

@app.route("/api/v1/login", methods=["POST"])
@log_request
def login():
    return login.login()

@app.route("/api/v1/signup", methods=["POST"])
@log_request
def signup():
    return signup.signup()

@app.route("/api/v1/protected", methods=["GET"])
@token_required
@log_request
def protected(current_user):
    return jsonify({"message": f"Hello, {current_user['name']}!", "statusCode": 200})

@app.route('/api/v1/start_trading', methods=['POST'])
@token_required
@log_request
def api_start_trading():
    result = start_trading()
    return jsonify({"message": result})

@app.route('/api/v1/stop_trading', methods=['POST'])
@token_required
@log_request
def api_stop_trading():
    result = stop_trading()
    return jsonify({"message": result})

@app.route("/dashboard", methods=["GET"])
@token_required
@log_request
def dashboard(current_user):
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
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"Message": "Email is required", "statusCode": 400})
    return jsonify(password_reset.request_password_reset(email))

@app.route("/api/v1/reset-password", methods=["POST"])
@log_request
def reset_password():
    data = request.get_json()
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')
    if not reset_token or not new_password:
        return jsonify({"Message": "Reset token and new password are required", "statusCode": 400})
    return jsonify(password_reset.reset_password(reset_token, new_password))

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
    
@app.route("/api/v1/get-candlestick_data", methods=["POST"])
@token_required
@log_request
def get_candlestick_data():
    return fetch_candlesticks_data()

handle_errors(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
