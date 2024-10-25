from db.mongo_conn import create as create_mongo_conn
from tokenz import tokens
import bcrypt
from bson import ObjectId


def login(msg_received):
    try:
        key = str(msg_received['key'])
        plain_password = str(msg_received["password"]).encode('utf-8')
    except KeyError:
        return {"Message": "A key is missing", "statusCode": 401}

    try:
        # Connect to MongoDB
        client = create_mongo_conn()
        db = client['exodus']
        users_collection = db.users

        # Find user by key
        user = users_collection.find_one({"key": key})

        if user:
            user_id = str(user['_id'])
            locator = str(user.get('locator', ''))
            hashed_password = user['password']

            if bcrypt.checkpw(plain_password, hashed_password):
                tkn = str(tokens.generate_token(user_id, locator))
                
                # Fetch user data from MongoDB
                user_info = db.personal_information.find_one({"users_id": ObjectId(user_id)})
                registration = user_info.get('registration', {}) if user_info else {}

                client.close()
                return {"Message": "Sign in successful", "token": tkn, "registration": registration, "statusCode": 200}
            else:
                client.close()
                return {"Message": "Wrong login details provided", "statusCode": 404}
        else:
            client.close()
            return {"Message": "Wrong login details provided", "statusCode": 404}

    except Exception as e:
        return {'Message': 'Error Logging in', 'statusCode': 600, 'Error': str(e)}
