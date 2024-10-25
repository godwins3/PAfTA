import bcrypt
import json
from utils.checkers.check import check_email, check_phone
from db.mongo_conn import create as create_mongo_conn
import pymongo
from tokenz.tokens import generate_locator, generate_db_name, generate_token
from utils.checkers.check import phone_char
from datetime import datetime

def user_register(msg_received):
    try:
        fname = msg_received['fullname']
        key = msg_received['key']
        terms = msg_received['TnC']
        form = msg_received['form']

        try:
            password = bcrypt.hashpw(msg_received["password"].encode("utf-8"), bcrypt.gensalt())
        except Exception as e:
            return {"Message": f"Error hashing password: {e}"}

        # if form == 'phoneNumber':
        #     phone_number = phone_char(key)
        #     checkp = json.loads(check_phone({"phoneNumber": phone_number}))
        #     if len(phone_number) < 9:
        #         return {"Message": "Invalid phone number", "statusCode": 401}

        #     if checkp["phone"] == '1':
        #         return {"Message": "phone number already in use.", "statusCode": 401}
        
        # elif form == 'email':
        #     checke = check_email(msg_received)
        #     if checke['email'] == "1":
        #         return {"Message": "Email already in use.", "statusCode": 401}
        # else:
        #     return {"Message": "Invalid form type", "statusCode": 401}

    except KeyError as k:
        return {"Message": "A key is missing for registrations", "Error": str(k), "statusCode": 401}

    client = create_mongo_conn()

    try:
        # Create an account for the users
        locator = str(generate_locator())
        db_name = generate_db_name()

        # Use the 'users' collection in the main database
        main_db = client['exodus']
        users_collection = main_db['users']

        # Insert user data into the 'users' collection
        user_data = {
            'key': key,
            'password': password,
            'locator': locator,
            'location': 'KE',
            'date': str(datetime.now())
        }
        result = users_collection.insert_one(user_data)
        users_id = result.inserted_id

        # Create the user's personal database
        db = client[db_name]
        personal_info_collection = db["personal_information"]
        personal_info = {
            'users_id': users_id,
            'fname': fname,
            'locator': locator,
            'Tnc': terms
        }
        personal_info_collection.insert_one(personal_info)

        # Generate token
        tkn = str(generate_token(str(users_id), locator))

        client.close()
        return {"Message": "Account created", "token": tkn, "statusCode": 200}

    except pymongo.errors.DuplicateKeyError:
        client.close()
        return {"Message": "Account already exists", "statusCode": 409}
    except Exception as e:
        client.close()
        print(e)
        return {"Message": "Account not created", "Error": str(e), "statusCode": 500}
