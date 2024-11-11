import random
from datetime import datetime
from notification_service.emails.service import send_verification_email
from utils.checkers.check import valid_email
from users.auth.signup import register
from db.mongo_conn import create as create_mongo_conn
from tokenz.tokens import generate_registration_verification_token, generate_registration_token, get_registration_verification_data
import string

# MongoDB connection
client = create_mongo_conn()
db = client['exodus']

def send(msg_received):
    try:
        email = msg_received['key']
        password = msg_received['password']

        if valid_email(email) == 0:
            return {"Message": "Invalid Email", "statusCode": 401}

    except KeyError:
        return {"Message": "A key is missing for email verification", "statusCode": 401}

    code = random.randint(1000, 9999)
    current_date = datetime.now()

    users = db.users.find_one({"email": email})

    if not users:
        reg_verification = db.reg_verification.find_one({"email": email})

        if not reg_verification:
            res = send_verification_email.send(email, code)

            if res["statusCode"] == 200:
                db.reg_verification.insert_one({
                    "email": email,
                    "phone_number": 0,
                    "code": code,
                    "date": current_date,
                    "counts": 1,
                    "createdOn": current_date,
                    "state": "unverified",
                    "method": "email"
                })
                res.update({'token': generate_registration_verification_token('email', email, password)})

            return res

        else:
            pass
            # ... (rest of the logic remains similar, just use MongoDB operations)

    else:
        return {'Message': 'Email is already taken.', 'statusCode': 200}

def verify(msg_received, header):
    reg_token = get_registration_verification_data(header)
    # print(reg_token)
    if reg_token == 0:
        return {"Message": "Invalid token provided for verification, restart the process.", "statusCode": 401}

    try:
        code = msg_received['code']
        form = reg_token['form']
        key = reg_token['key']
        password = reg_token['password']
        # print(form, key)
    except KeyError:
        return {"Message": "A key is missing for code verification", "statusCode": 401}

    if form.lower() == 'email':
        reg_verification = db.reg_verification.find_one({"email": key, "code": code})

        new_code = random.randint(1000, 9999)

        if reg_verification:
            db.reg_verification.update_one(
                {"email": key, "code": code},
                {"$set": {"state": "verified", "code": new_code}}
            )

            x = {
                "subject": "register_normal",
                "displayName": random_string(),
                "about": "I love Green Oases!",
                "password": password,
                "location": [],
                "country": "KE",
                "gender": "male",
                "over18": 1,
            }
            res = dict(register.register(x, header))

            if res["statusCode"] == 200:
                return {"Message": "Your email has been verified", "token": res["token"], "statusCode": 200}
            else:
                return {"Message": "Your email has been verified, but there was an error in registering you.",
                        "statusCode": 500}

        else:
            return {"Message": "Wrong details provided", "statusCode": 401}

    else:
        return {"Message": "Wrong form provided", "statusCode": 401}


def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
