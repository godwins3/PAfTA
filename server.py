from flask import Flask
from users.auth import login, signup

app = Flask(__name__)

@app.route("/")
def exodus():
    return "<p>Hello, World!</p>"

@app.route("/api/v1/login", methods=["POST"])
def login():
    return login.login()

@app.route("/api/v1/signup", methods=["POST"])
def signup():
    return signup.signup()

if __name__ == "__main__":
    app.run(debug=True)

