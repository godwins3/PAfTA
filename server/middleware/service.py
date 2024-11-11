import jwt
from functools import wraps
from flask import request, jsonify
from config.config import secret_config
from db.mongo_conn import create as create_mongo_conn
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Get the secret key for JWT
secret_key = secret_config()["secret_key"]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in the header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            # Get the user from the database
            client = create_mongo_conn()
            db = client['exodus']
            users_collection = db['users']
            current_user = users_collection.find_one({"_id": data['sub']})
            client.close()

            if not current_user:
                return jsonify({'message': 'User not found!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Pass the current user to the route
        return f(current_user, *args, **kwargs)

    return decorated

def log_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Log the request
        logging.info(f"{datetime.now()} - {request.method} {request.url}")
        return f(*args, **kwargs)
    return decorated

def handle_errors(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal server error'}), 500

# Usage in routes
# @app.route('/protected')
# @token_required
# @log_request
# def protected(current_user):
#     return jsonify({'message': f'Hello {current_user["name"]}!'})

