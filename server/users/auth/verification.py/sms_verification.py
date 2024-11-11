import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from notification_service.sms.service import send_verification_sms
from utils.checkers.check import disallowed_characters
from tokenz.tokens import generate_registration_verification_token, generate_registration_token, get_registration_verification_data
from users.auth.signup import normal_registration
import string

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']

def send(msg_received):
    try:
        phone_number = disallowed_characters.phone_char(str(msg_received['key']))
        password = msg_received['password']
    except KeyError:
        return {"Message": "A key is missing for SMS verification", "statusCode": 401}

    code = random.randint(1000, 9999)
    current_date = datetime.now()

    # Check if phone number is already verified
    if db.users.find_one({"phone_number": phone_number}):
        return {'Message': 'Phone number is verified, kindly log in.', 'statusCode': 401}

    # Check existing verification attempts
    reg_verification = db.reg_verification.find_one({"phone_number": phone_number})

    if not reg_verification:
        res = send_verification_sms.send(phone_number, code)
        if res["statusCode"] == 200:
            db.reg_verification.insert_one({
                "email": "",
                "phone_number": phone_number,
                "code": code,
                "date": current_date,
                "counts": 1,
                "createdOn": current_date,
                "state": "unverified",
                "method": "phoneNumber"
            })
            res.update({'token': generate_registration_verification_token('phoneNumber', phone_number, password)})
        return res
    else:
        pass
        # ... (rest of the logic for existing verification attempts)
        # You'll need to update this part to use MongoDB operations

def verify(msg_received, header):
    reg_token = get_registration_verification_data(header)
    if reg_token == 0:
        return {"Message": "Invalid token provided for verification, restart the process.", "statusCode": 401}
    try:
        code = msg_received['code']
        form = reg_token['form']
        key = reg_token['key']
        password = reg_token['password']
    except KeyError:
        return {"Message": "A key is missing for code verification", "statusCode": 401}

    if form.lower() == 'phonenumber':
        reg_verification = db.reg_verification.find_one({"phone_number": key, "code": code})

        if reg_verification:
            new_code = random.randint(1000, 9999)
            db.reg_verification.update_one(
                {"phone_number": key, "code": code},
                {"$set": {"state": "verified", "code": new_code}}
            )

            x = {
                "subject": "register_normal",
                "displayName": random_string(),
                "about": "I love Exodus",
                "password": password,
                "location": [],
                "country": "KE",
                "gender": "male",
                "birthday": 763679927000,
                "over18": 1,
                "interestedIn": "female",
                "interest": ['running', 'swimming', 'dancing'],
            }
            res = normal_registration.register(x, header)
            
            if res['statusCode'] == 200:
                return {"Message": "Your phone number has been verified", "token": res["token"], "statusCode": 200}
            else:
                return {"Message": "Your phone has been verified, but there was an error in registering you.", "statusCode": 500}
        else:
            return {"Message": "Wrong details provided", "statusCode": 401}
    else:
        return {"Message": "Wrong form provided", "statusCode": 401}

def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
