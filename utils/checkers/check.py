import json
import re
from db.mongo_conn import create as create_mongo_conn
from tokenz.tokens import get_id


def check_email(msg_received):
    email = str(msg_received["key"])

    if email == '0':
        return json.dumps({'phone': '0'})

    # Connect to MongoDB
    client = create_mongo_conn()
    db = client['exodus']
    users_collection = db['users']

    # Check if the email exists in the users collection
    user = users_collection.find_one({'email': email})

    # Close the MongoDB connection
    client.close()

    if user:
        return json.dumps({'email': '1'})
    else:
        return json.dumps({'email': '0'})
    
def valid_email(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, str(email)):

        return 1

    else:
        return 0

def check_phone(msg_received):
    phone = str(msg_received["key"])

    if phone == '0':
        return json.dumps({'phone': '0'})
    
    client = create_mongo_conn()
    db = client['exodus']
    users_collection = db['users']

    # Check if the phone exists in the users collection
    user = users_collection.find_one({'phone': phone})

    client.close()

    if user:
        return json.dumps({'phone': '1'})
    else:
        return json.dumps({'phone': '0'})
        
def disallowed(string: str):
    # This is for names
    disallowed_characters = "^}{=~,[<>]/*-;+/:()%$#@!|/?_\'\"`.1234567890"
    _name = string.lower()
    for character in disallowed_characters:
        _name = _name.replace(character, "")

    __name = list(_name)
    first_character = _name[0].upper()
    __name[0] = first_character
    _name = ''.join(__name)

    return _name


def not_allowed(string: str):
    # This is for strings
    disallowed_characters = "^}{=~,[<>]/*-;+/:()%$#@!|/?_\'\"`.1234567890"
    _name = string
    for character in disallowed_characters:
        _name = _name.replace(character, "")

    return _name


def phone_char(string: str):
    # This is for phone numbers
    disallowed_characters = "^}{=~,[<>]/*-;/:()%$#@!|/?_\'\"`"
    _number = string
    for character in disallowed_characters:
        _number = _number.replace(character, "")

    _number = re.sub('[A-Za-z]', '', _number)

    return _number

def check_token(header):
    users_id = get_id(header)
    if not str(users_id).isdigit():
        return {"status": 0, "users_id": 0}
    else:
        return {"status": 1, "users_id": users_id}