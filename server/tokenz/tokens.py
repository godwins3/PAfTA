from datetime import datetime, timedelta
import jwt
from db.mongo_conn import create as create_mongo_conn
# from tokenz import secret_config, picture_code
from config.config import secret_config, quickgen_secret_config
import random
import secrets
import string

the_key = secret_config()
my_string = the_key["secret_key"]

the_quick_key = quickgen_secret_config()
the_quick_string = the_quick_key["secret_key"]

# MongoDB connection
client = create_mongo_conn()
db = client['exodus']
users_collection = db['users']

def get_user(user_id, locator):
    try:
        user = users_collection.find_one({"user_id": user_id, "locator": locator})
        return 1 if user else 0
    except Exception:
        return 0

def generate_token(user_id, locator):
    try:

        payload = {
            'exp': datetime.utcnow() + timedelta(days=30, seconds=0),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'string': locator
        }
        return jwt.encode(
            payload,
            my_string,
            algorithm='HS256'
        )
    except Exception as e:
        return 0


def quick_gen(the_token):
    try:

        payload = jwt.decode(the_token, the_quick_string, algorithm='HS256')
        user_id = payload['sub']
        locator = payload['string']
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=80),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'string': locator
        }
        return jwt.encode(
            payload,
            my_string,
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as e:
        return e

def generate_registration_token(form: str, key: str):
    try:
        the_key = secret_config.secret_config(section='reg_token')
        my_string = the_key["secret_key"]

        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
            'iat': datetime.utcnow(),
            'form': form,
            'key': key
        }
        return jwt.encode(
            payload,
            my_string,
            algorithm='HS256'
        )
    except Exception as e:
        return 0


def get_registration_data(auth_token):
    try:
        the_key = secret_config.secret_config(section='reg_token')
        my_string = the_key["secret_key"]
        payload = jwt.decode(auth_token, my_string, algorithms='HS256')
        form = payload['form']
        key = payload['key']

        return {'form': form, 'key': key}

    except jwt.ExpiredSignatureError as e:

        return 0
    except jwt.InvalidTokenError as e:

        return 0


# This token contains the form and key and password field
def generate_registration_verification_token(form: str, key: str, password: str):
    try:
        the_key = secret_config.secret_config(section='reg_token')
        my_string = the_key["secret_key"]

        payload = {
            'exp': datetime.utcnow() + timedelta(days=2, seconds=0),
            'iat': datetime.utcnow(),
            'form': form,
            'key': key,
            'password': password
        }
        return jwt.encode(
            payload,
            my_string,
            algorithm='HS256'
        )
    except Exception as e:
        return 0

# The return value contains the form and key and password field
def get_registration_verification_data(auth_token):
    try:
        the_key = secret_config.secret_config(section='reg_token')
        my_string = the_key["secret_key"]
        payload = jwt.decode(auth_token, my_string, algorithms='HS256')
        form = payload['form']
        key = payload['key']
        password = payload['password']

        return {'form': form, 'key': key, 'password': password}

    except jwt.ExpiredSignatureError as e:

        return 0
    except jwt.InvalidTokenError as e:

        return 0


def get_id(auth_token):
    try:
        payload = jwt.decode(auth_token, my_string, algorithms='HS256')
        _id = int(payload['sub'])
        locator = payload['string']
        key = str(get_user(_id, locator))
        if key == '1':
            return _id
        else:
            return "Error invalid token"
    except jwt.ExpiredSignatureError:
        return "Error expired token"
    except jwt.InvalidTokenError:
        return "Error invalid token"

# GENERATING DB NAME
def generate_db_name():
    code = random.randint(1, 1000)
    return check_db_name(code)

def check_db_name(code: int):
    # Get the total count of documents in the collection
    total_records = users_collection.count_documents({})
    
    db = total_records + code
    if len(str(db)) < 6:
        db = f'{(6 - len(str(db))) * "0"}{db}'
    db = f'T{db}'

    # Check if the generated db name already exists
    existing_db = users_collection.find_one({'database_name': db})

    if existing_db:
        # If the db name already exists, generate a new one
        return generate_db_name()
    else:
        # If the db name is unique, return it
        return db

# GENERATING LOCATOR
def generate_locator():
    code = str(user_locator())
    return check_locator(code)

def check_locator(code: str):
    # Check if the generated locator already exists
    existing_user = users_collection.find_one({'locator': code})

    if existing_user:
        # If the locator already exists, generate a new one
        return generate_locator()
    else:
        # If the locator is unique, return it
        return code

# Close the MongoDB connection when the application shuts down
def close_mongodb_connection():
    client.close()


def generate_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(7))
        if (any(c.islower() for c in password) and any(c.isupper()
                                                       for c in password) and sum(c.isdigit() for c in password) >= 3):
            return password.upper()


def forgot_pass():
    alphabet = string.ascii_letters.upper() + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(6))
        if (any(c.isupper()
                for c in password) and sum(c.isdigit() for c in password) >= 5):
            return password.upper()


def reset_post_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password) and any(c.isupper()
                                                       for c in password) and sum(c.isdigit() for c in password) >= 3):
            return password.upper()


def user_locator():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(9))
        if (any(c.islower() for c in password) and any(c.isupper()
                                                       for c in password) and sum(c.isdigit() for c in password) >= 5):
            return password.upper()


def user_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(11))
        if (any(c.islower() for c in password) and any(c.isupper()
                                                       for c in password) and sum(c.isdigit() for c in password) >= 8):
            return password.upper()

def generate_password_reset_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'type': 'password_reset'
        }
        return jwt.encode(
            payload,
            my_string,
            algorithm='HS256'
        )
    except Exception as e:
        return 0

def verify_password_reset_token(token):
    try:
        payload = jwt.decode(token, my_string, algorithms=['HS256'])
        if payload['type'] != 'password_reset':
            return None
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
