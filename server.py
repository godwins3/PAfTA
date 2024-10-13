from flask import Flask, jsonify
from users.auth import login, signup
from middleware.service import token_required, log_request, handle_errors

app = Flask(__name__)

@app.route("/")
def exodus():
    return "<p>Hello, World!</p>"

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

handle_errors(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
